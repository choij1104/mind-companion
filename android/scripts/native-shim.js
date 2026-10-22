/* Mind Companion — Google Play build only.
   Android WebView has no Web Speech API and ignores <a download>. When the app runs inside the
   native shell (Capacitor), this file provides:
     - window.SpeechRecognition  (on @capacitor-community/speech-recognition)
     - window.speechSynthesis + SpeechSynthesisUtterance  (on @capacitor-community/text-to-speech)
     - <a download> clicks -> file written to the cache and handed to the Android share sheet
   The app's own code is unchanged and uses the standard web APIs. In a browser this file does nothing. */
(function () {
  "use strict";
  var C = window.Capacitor;
  if (!C || !C.isNativePlatform || !C.isNativePlatform()) return;

  var SR = C.registerPlugin("SpeechRecognition");
  var TTS = C.registerPlugin("TextToSpeech");
  var FS = C.registerPlugin("Filesystem");
  var Share = C.registerPlugin("Share");

  /* ---------- speech in ---------- */
  function NativeRecognition() {
    this.lang = "en-US"; this.continuous = false; this.interimResults = false; this.maxAlternatives = 1;
    this.onstart = null; this.onresult = null; this.onerror = null; this.onend = null;
    this._active = false; this._handles = []; this._last = "";
  }
  function fire(rec, name, ev) { try { if (typeof rec[name] === "function") rec[name](ev || {}); } catch (e) {} }
  function resultEvent(text, isFinal) {
    var alt = { transcript: text, confidence: 0.9 };
    var res = [alt]; res.isFinal = !!isFinal;
    var results = [res];
    return { resultIndex: 0, results: results };
  }
  NativeRecognition.prototype._cleanup = function () {
    this._handles.forEach(function (h) { try { h.remove(); } catch (e) {} });
    this._handles = [];
  };
  NativeRecognition.prototype._finish = function () {
    if (!this._active) return;
    this._active = false; this._cleanup();
    if (this._last) fire(this, "onresult", resultEvent(this._last, true));
    fire(this, "onend");
  };
  NativeRecognition.prototype.start = function () {
    var self = this;
    if (self._active) return;
    self._active = true; self._last = "";
    (async function () {
      try {
        var avail = await SR.available();
        if (!avail || !avail.available) { self._active = false; fire(self, "onerror", { error: "service-not-allowed" }); fire(self, "onend"); return; }
        var perm = await SR.checkPermissions();
        if (!perm || perm.speechRecognition !== "granted") perm = await SR.requestPermissions();
        if (!perm || perm.speechRecognition !== "granted") { self._active = false; fire(self, "onerror", { error: "not-allowed" }); fire(self, "onend"); return; }
        self._handles.push(await SR.addListener("partialResults", function (d) {
          var m = d && d.matches && d.matches[0];
          if (m) { self._last = m; if (self.interimResults) fire(self, "onresult", resultEvent(m, false)); }
        }));
        self._handles.push(await SR.addListener("listeningState", function (d) {
          if (d && d.status === "stopped") setTimeout(function () { self._finish(); }, 150);
        }));
        fire(self, "onstart");
        await SR.start({ language: self.lang || "en-US", maxResults: self.maxAlternatives || 1, partialResults: true, popup: false });
      } catch (e) {
        var msg = String((e && e.message) || e || "");
        self._cleanup(); self._active = false;
        fire(self, "onerror", { error: /no match|no speech|didn't|timeout/i.test(msg) ? "no-speech" : "aborted" });
        fire(self, "onend");
      }
    })();
  };
  NativeRecognition.prototype.stop = function () { var self = this; SR.stop().catch(function () {}).then(function () { self._finish(); }); };
  NativeRecognition.prototype.abort = function () { this._last = ""; this.stop(); };
  window.SpeechRecognition = NativeRecognition;
  window.webkitSpeechRecognition = NativeRecognition;

  /* ---------- speech out ---------- */
  function Utterance(text) { this.text = text || ""; this.lang = ""; this.rate = 1; this.pitch = 1; this.volume = 1; this.voice = null; this.onend = null; this.onerror = null; }
  var synth = {
    speaking: false, pending: false, paused: false, onvoiceschanged: null, _voices: [],
    getVoices: function () { return this._voices; },
    speak: function (u) {
      var s = this; s.speaking = true;
      TTS.speak({ text: u.text, lang: u.lang || (u.voice && u.voice.lang) || "en-US", rate: u.rate || 1, pitch: u.pitch || 1, volume: u.volume == null ? 1 : u.volume, category: "playback" })
        .then(function () { s.speaking = false; if (typeof u.onend === "function") u.onend({}); })
        .catch(function (e) { s.speaking = false; if (typeof u.onerror === "function") u.onerror({ error: String(e) }); });
    },
    cancel: function () { this.speaking = false; TTS.stop().catch(function () {}); },
    pause: function () {}, resume: function () {}
  };
  TTS.getSupportedVoices().then(function (r) {
    synth._voices = ((r && r.voices) || []).map(function (v) { return { name: v.name, lang: v.lang, voiceURI: v.voiceURI, localService: v.localService, default: v.default }; });
    if (typeof synth.onvoiceschanged === "function") synth.onvoiceschanged();
  }).catch(function () {});
  try { Object.defineProperty(window, "speechSynthesis", { value: synth, configurable: true }); } catch (e) { window.speechSynthesis = synth; }
  window.SpeechSynthesisUtterance = Utterance;

  /* ---------- <a download> -> share sheet ---------- */
  function blobToBase64(blob) {
    return new Promise(function (res, rej) { var r = new FileReader(); r.onload = function () { res(String(r.result).split(",")[1] || ""); }; r.onerror = rej; r.readAsDataURL(blob); });
  }
  var origClick = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () {
    var a = this;
    if (!a.hasAttribute("download") || !a.href) return origClick.call(a);
    var name = (a.getAttribute("download") || "mind-companion-file").replace(/[\\/:*?"<>|]+/g, "-");
    fetch(a.href).then(function (r) { return r.blob(); }).then(blobToBase64).then(function (data) {
      return FS.writeFile({ path: name, data: data, directory: "CACHE" });
    }).then(function (w) {
      return Share.share({ title: name, files: [w.uri] });
    }).catch(function (e) {
      if (!/cancel/i.test(String((e && e.message) || e))) { try { alert(name + ": could not save the file."); } catch (x) {} }
    });
  };
})();
