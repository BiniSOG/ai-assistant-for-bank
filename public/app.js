/* Dashen Bank AI Account Assistant – front end (vanilla JS, no build step). */
(() => {
  "use strict";

  // ------------------------------------------------------------------ i18n
  const UI = {
    en: {
      welcome: "Welcome to<br>Dashen Bank<br>Super App", create: "Create Account", login: "Login",
      send: "Send Money", bills: "Pay Bills", topup: "Mobile Top-up", more: "More",
      promo: "Open your account in minutes with <b>AI Video Assistant</b>",
      aiAssistant: "AI Account Assistant", startYes: "Yes, let's get started", send2: "Send",
      confirm: "Confirm", orSpeak: "or answer by voice 🎙", fanLabel: "FAN (National ID Number)",
      continue: "Continue", otpTitle: "Verify with OTP", noOtp: "Didn't receive the OTP?",
      verifyOtp: "Verify OTP", reviewTitle: "Confirm Your Information",
      reviewText: "We retrieved the following details from the National ID database. Please review and confirm.",
      edit: "Edit", confirmCreate: "Confirm & Create Account", creatingTitle: "Creating Your Account…",
      successTitle: "Account Created Successfully! 🎉",
      successText: "Your Dashen Bank account is now active. You can start using it immediately.",
      acctNo: "Account Number", acctType: "Account Type", goAccount: "Go to My Account",
      download: "⤓ Download Account Details", resend: "Resend", typeName: "Type your full name…",
      typeAnswer: "Type your answer…", cityPh: "Addis Ababa", natPh: "Ethiopian", acctPh: "Savings Account",
      otpText: "We've sent a one-time password (OTP) to your registered mobile number from National ID",
      demoOtp: "Demo mode – no SMS gateway. Your OTP is", demoOnly: "Demo: only “Create Account” is available.",
      fullName: "Full Name", dob: "Date of Birth", city: "Birth City", nationality: "Nationality",
      fan: "FAN", type: "Account Type", mismatch: "Differs from what you told the assistant",
      mismatchNote: "Some details differ from what you told the assistant. The National ID record will be used.",
      endCall: "End the call and return to the home screen?", copied: "Account number copied",
      noSpeech: "Voice input isn't supported in this browser – please type instead.",
      progress: ["Verifying identity (National ID)", "Retrieving your details", "Creating Dashen Bank account", "Setting up your profile"],
      you: "You",
    },
    am: {
      welcome: "እንኳን ወደ<br>ዳሽን ባንክ<br>ሱፐር አፕ በደህና መጡ", create: "ሂሳብ ይክፈቱ", login: "ይግቡ",
      send: "ገንዘብ ይላኩ", bills: "ክፍያዎች", topup: "የአየር ሰዓት", more: "ተጨማሪ",
      promo: "በ<b>AI ቪዲዮ ረዳት</b> በደቂቃዎች ውስጥ ሂሳብዎን ይክፈቱ",
      aiAssistant: "AI የሂሳብ ረዳት", startYes: "አዎ፣ እንጀምር", send2: "ላክ", confirm: "አረጋግጥ",
      orSpeak: "ወይም በድምጽ ይመልሱ 🎙", fanLabel: "FAN (የብሔራዊ መታወቂያ ቁጥር)", continue: "ቀጥል",
      otpTitle: "በOTP ያረጋግጡ", noOtp: "OTP አልደረሰዎትም?", verifyOtp: "OTP አረጋግጥ",
      reviewTitle: "መረጃዎን ያረጋግጡ",
      reviewText: "የሚከተለውን መረጃ ከብሔራዊ መታወቂያ የመረጃ ቋት አግኝተናል። እባክዎ ይገምግሙ እና ያረጋግጡ።",
      edit: "አስተካክል", confirmCreate: "አረጋግጥ እና ሂሳብ ክፈት", creatingTitle: "ሂሳብዎ እየተከፈተ ነው…",
      successTitle: "ሂሳብዎ በተሳካ ሁኔታ ተከፍቷል! 🎉",
      successText: "የዳሽን ባንክ ሂሳብዎ አሁን ንቁ ነው። ወዲያውኑ መጠቀም ይችላሉ።",
      acctNo: "የሂሳብ ቁጥር", acctType: "የሂሳብ አይነት", goAccount: "ወደ ሂሳቤ ሂድ",
      download: "⤓ የሂሳብ መረጃ አውርድ", resend: "እንደገና ላክ", typeName: "ሙሉ ስምዎን ይጻፉ…",
      typeAnswer: "መልስዎን ይጻፉ…", cityPh: "አዲስ አበባ", natPh: "ኢትዮጵያዊ", acctPh: "ቁጠባ",
      otpText: "በብሔራዊ መታወቂያ ወደተመዘገበው ስልክ ቁጥርዎ የአንድ ጊዜ የይለፍ ቃል (OTP) ልከናል",
      demoOtp: "የሙከራ ሁነታ – SMS የለም። OTP-ዎ", demoOnly: "ሙከራ፦ “ሂሳብ ይክፈቱ” ብቻ ይሰራል።",
      fullName: "ሙሉ ስም", dob: "የትውልድ ቀን", city: "የትውልድ ከተማ", nationality: "ዜግነት",
      fan: "FAN", type: "የሂሳብ አይነት", mismatch: "ለረዳቱ ከነገሩት የተለየ ነው",
      mismatchNote: "አንዳንድ መረጃዎች ለረዳቱ ከነገሩት ይለያሉ። የብሔራዊ መታወቂያው መረጃ ጥቅም ላይ ይውላል።",
      endCall: "ጥሪውን ጨርሰው ወደ መነሻ ገጽ ይመለሱ?", copied: "የሂሳብ ቁጥሩ ተቀድቷል",
      noSpeech: "ይህ አሳሽ የድምጽ ግብዓትን አይደግፍም – እባክዎ ይጻፉ።",
      progress: ["ማንነትን በማረጋገጥ ላይ (ብሔራዊ መታወቂያ)", "መረጃዎን በማምጣት ላይ", "የዳሽን ባንክ ሂሳብ በመክፈት ላይ", "መገለጫዎን በማዘጋጀት ላይ"],
      you: "እርስዎ",
    },
  };
  const CHOICES = {
    birth_city: { en: ["Addis Ababa", "Dire Dawa", "Bahir Dar", "Hawassa", "Mekelle", "Gondar", "Adama"], am: ["አዲስ አበባ", "ድሬ ዳዋ", "ባህር ዳር", "ሀዋሳ", "መቀሌ", "ጎንደር", "አዳማ"], ico: "📍" },
    nationality: { en: ["Ethiopian", "Kenyan", "Eritrean", "Djiboutian"], am: ["ኢትዮጵያዊ", "Kenyan", "Eritrean", "Djiboutian"], ico: "🌍" },
    account_type: { en: ["Savings Account", "Current Account", "Interest-Free (Wadiah) Savings", "Fixed Time Deposit"], am: ["ቁጠባ", "ተንቀሳቃሽ", "ከወለድ ነፃ (ወዲአህ) ቁጠባ", "የጊዜ ገደብ ተቀማጭ"], ico: "🏦" },
  };

  // ------------------------------------------------------------------ app state
  const S = { lang: "en", state: null, token: null, view: null, muted: false, captions: true, busy: false, stream: null, timer: null, resendTimer: null, extra: {} };
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const L = (k) => UI[S.lang][k] ?? UI.en[k];

  function applyI18n() {
    document.documentElement.lang = S.lang;
    $$("[data-i18n]").forEach((el) => { el.innerHTML = L(el.dataset.i18n); });
    $$(".lang-toggle button").forEach((b) => b.classList.toggle("on", b.dataset.lang === S.lang));
  }

  function toast(msg) {
    const t = $("#toast"); t.textContent = msg; t.classList.add("show");
    clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove("show"), 2600);
  }

  function show(id) {
    $$(".screen").forEach((s) => s.classList.toggle("active", s.id === `screen-${id}`));
  }

  const ORDER = ["home", "greeting", "full_name", "date_of_birth", "birth_city", "fan", "otp", "review", "creating", "done"];
  function journey(step) {
    const map = { nationality: "birth_city", account_type: "birth_city" };
    const idx = ORDER.indexOf(map[step] || step);
    $$("#journey li").forEach((li) => {
      const i = ORDER.indexOf(li.dataset.s);
      li.classList.toggle("done", i < idx); li.classList.toggle("now", i === idx);
    });
  }

  // ------------------------------------------------------------------ API
  async function api(path, body) {
    const res = await fetch(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) { const e = new Error(data.detail || `HTTP ${res.status}`); e.status = res.status; throw e; }
    return data;
  }
  const signed = (extra = {}) => ({ state: S.state, token: S.token, ...extra });

  async function call(path, body) {
    if (S.busy) return null;
    S.busy = true; setBusy(true);
    try {
      const data = await api(path, body);
      S.state = data.state; S.token = data.token; S.view = data.view; S.extra = data.extra || {};
      return data;
    } catch (e) {
      console.error(e);
      if (e.status === 400) { toast("Session expired – restarting"); setTimeout(goHome, 800); }
      else toast(e.message || "Network error");
      return null;
    } finally { S.busy = false; setBusy(false); }
  }
  function setBusy(on) {
    $("#bubble").classList.toggle("thinking", on && $("#screen-call").classList.contains("active"));
    $$("button.btn.primary").forEach((b) => (b.disabled = on));
  }

  // ------------------------------------------------------------------ assistant voice (TTS)
  function pickVoice() {
    if (!("speechSynthesis" in window)) return null;
    const voices = speechSynthesis.getVoices();
    const want = S.lang === "am" ? ["am"] : ["en-GB", "en-US", "en"];
    for (const w of want) {
      const fem = voices.find((v) => v.lang.startsWith(w) && /female|samantha|zira|libby|sonia|aria|jenny/i.test(v.name));
      const any = voices.find((v) => v.lang.startsWith(w));
      if (fem || any) return fem || any;
    }
    return null;
  }
  function say(text, userText) {
    const b = $("#bubble");
    b.innerHTML = "";
    if (userText) { const y = document.createElement("span"); y.className = "you"; y.textContent = `${L("you")}: “${userText}”`; b.append(y); }
    b.append(document.createTextNode(text));
    b.classList.toggle("hidden", !S.captions);
    const avatar = $("#avatar");
    const clean = text.replace(/[\u{1F300}-\u{1FAFF}]/gu, "");
    const fallbackTalk = () => { avatar.classList.add("talking"); clearTimeout(say._t); say._t = setTimeout(() => avatar.classList.remove("talking"), Math.min(6000, 60 * clean.length)); };
    if (S.muted || !("speechSynthesis" in window)) return fallbackTalk();
    const voice = pickVoice();
    if (S.lang === "am" && !voice) return fallbackTalk(); // no Amharic voice installed
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(clean);
    if (voice) { u.voice = voice; u.lang = voice.lang; }
    u.rate = 1.02;
    u.onstart = () => avatar.classList.add("talking");
    u.onend = u.onerror = () => avatar.classList.remove("talking");
    speechSynthesis.speak(u);
  }

  // ------------------------------------------------------------------ customer voice (STT)
  const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
  let rec = null;
  function listen() {
    if (!Rec) { toast(L("noSpeech")); return; }
    if (rec) { rec.stop(); return; }
    if ("speechSynthesis" in window) speechSynthesis.cancel();
    rec = new Rec();
    rec.lang = S.lang === "am" ? "am-ET" : "en-US";
    rec.interimResults = true;
    rec.maxAlternatives = 1;
    const target = activeInput();
    $("#btnMic").classList.add("listening"); $("#wave").classList.add("on");
    let finalText = "";
    rec.onresult = (ev) => {
      let interim = "";
      for (const r of ev.results) (r.isFinal ? (finalText = r[0].transcript) : (interim += r[0].transcript));
      if (target) target.value = finalText || interim;
    };
    rec.onerror = (e) => { if (e.error !== "no-speech" && e.error !== "aborted") toast(`Mic: ${e.error}`); };
    rec.onend = () => {
      rec = null; $("#btnMic").classList.remove("listening"); $("#wave").classList.remove("on");
      if (finalText.trim()) sendMessage(finalText.trim());
    };
    rec.start();
  }
  function activeInput() {
    const pane = $(".pane.on");
    return pane && pane.querySelector("input:not([type=date])");
  }

  // ------------------------------------------------------------------ video call screen
  async function startCamera() {
    if (!navigator.mediaDevices?.getUserMedia) return;
    try {
      S.stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false });
      const v = $("#selfView"); v.srcObject = S.stream; v.hidden = false; $("#ccCam").classList.remove("off");
    } catch { $("#ccCam").classList.add("off"); }
  }
  function stopCamera() {
    S.stream?.getTracks().forEach((t) => t.stop()); S.stream = null;
    $("#selfView").hidden = true; $("#ccCam").classList.add("off");
  }
  function startTimer() {
    const t0 = Date.now(); clearInterval(S.timer);
    S.timer = setInterval(() => {
      const s = Math.floor((Date.now() - t0) / 1000);
      $("#callTimer").textContent = `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
    }, 1000);
  }

  function paneFor(step) {
    if (step === "greeting") return "greeting";
    if (step === "full_name") return "voice";
    if (step === "date_of_birth") return "date";
    if (step in CHOICES) return "choice";
    if (step === "fan") return "fan";
    return null;
  }

  function render() {
    const v = S.view; if (!v) return;
    journey(v.step);
    const p = paneFor(v.step);
    if (p) {
      show("call");
      $$(".pane").forEach((el) => el.classList.toggle("on", el.dataset.pane === p));
      if (p === "voice") { $("#inText").value = ""; $("#inText").placeholder = L("typeName"); }
      if (p === "date") { $("#inDate").max = new Date().toISOString().slice(0, 10); if (!$("#inDate").value) $("#inDate").value = "2000-01-15"; }
      if (p === "fan") $("#inFan").value = "";
      if (p === "choice") {
        const c = CHOICES[v.step];
        $("#choiceIco").textContent = c.ico;
        $("#inChoice").value = "";
        $("#inChoice").placeholder = L({ birth_city: "cityPh", nationality: "natPh", account_type: "acctPh" }[v.step]);
        const chips = $("#chips"); chips.innerHTML = "";
        c[S.lang].forEach((label, i) => {
          const b = document.createElement("button"); b.type = "button"; b.className = "chip"; b.textContent = label;
          b.onclick = () => sendMessage(c.en[i]); chips.append(b);
        });
      }
      return;
    }
    if (v.step === "otp") return showOtp();
    if (v.step === "review") return showReview();
    if (v.step === "creating") return runCreation();
    if (v.step === "done") return showDone();
  }

  async function beginCall() {
    show("call"); journey("greeting"); startTimer(); startCamera();
    $("#bubble").textContent = "";
    $$(".pane").forEach((el) => el.classList.remove("on"));
    const data = await call("/api/session/start", { lang: S.lang });
    if (!data) return;
    render(); say(data.reply);
  }

  async function sendMessage(text) {
    if (!text) return;
    const data = await call("/api/chat", signed({ message: text }));
    if (!data) return;
    render();
    if (S.view.step === "otp") return; // the OTP screen takes over
    say(data.reply, text);
  }

  function goHome() {
    if ("speechSynthesis" in window) speechSynthesis.cancel();
    rec?.abort(); stopCamera(); clearInterval(S.timer); clearInterval(S.resendTimer);
    S.state = S.token = S.view = null;
    show("home"); journey("home");
  }

  // ------------------------------------------------------------------ OTP
  function showOtp() {
    show("otp"); journey("otp");
    $("#otpText").textContent = `${L("otpText")} (${S.extra.phone || ""}).`;
    const demo = $("#demoOtp");
    if (S.extra.demo_otp) { demo.hidden = false; demo.innerHTML = `${L("demoOtp")} <b>${S.extra.demo_otp}</b>`; } else demo.hidden = true;
    $("#otpError").textContent = "";
    const boxes = $$("#otpBoxes input"); boxes.forEach((b) => (b.value = "")); boxes[0].focus();
    say(`${L("otpText")}.`);
    startResendCountdown(60);
  }
  function startResendCountdown(sec) {
    const btn = $("#btnResend"); let left = sec; btn.disabled = true;
    clearInterval(S.resendTimer);
    const tick = () => { btn.textContent = left > 0 ? `${L("resend")} (${left}s)` : L("resend"); btn.disabled = left > 0; left--; if (left < -1) clearInterval(S.resendTimer); };
    tick(); S.resendTimer = setInterval(tick, 1000);
  }
  function wireOtpBoxes() {
    const boxes = $$("#otpBoxes input");
    boxes.forEach((b, i) => {
      b.addEventListener("input", () => {
        b.value = b.value.replace(/\D/g, "").slice(-1);
        if (b.value && i < boxes.length - 1) boxes[i + 1].focus();
        if (boxes.every((x) => x.value)) $("#formOtp").requestSubmit();
      });
      b.addEventListener("keydown", (e) => { if (e.key === "Backspace" && !b.value && i > 0) boxes[i - 1].focus(); });
      b.addEventListener("paste", (e) => {
        const d = (e.clipboardData.getData("text") || "").replace(/\D/g, "").slice(0, 6);
        if (!d) return; e.preventDefault();
        d.split("").forEach((ch, j) => (boxes[j].value = ch));
        if (d.length === 6) $("#formOtp").requestSubmit();
      });
    });
  }
  async function verifyOtp(e) {
    e.preventDefault();
    const code = $$("#otpBoxes input").map((b) => b.value).join("");
    if (code.length !== 6) return;
    const data = await call("/api/otp/verify", signed({ code }));
    if (!data) return;
    if (S.view.step === "otp") {
      $("#otpError").textContent = data.reply;
      $$("#otpBoxes input").forEach((b) => (b.value = "")); $$("#otpBoxes input")[0].focus();
      return;
    }
    clearInterval(S.resendTimer);
    render(); say(data.reply);
  }

  // ------------------------------------------------------------------ review
  function fmtDate(iso) {
    if (!iso) return "";
    const d = new Date(iso + "T00:00:00");
    return d.toLocaleDateString(S.lang === "am" ? "am-ET" : "en-US", { year: "numeric", month: "short", day: "numeric" });
  }
  function showReview() {
    show("review"); journey("review");
    const v = S.view, id = v.identity || {};
    const rows = [
      ["👤", "fullName", id.full_name, "full_name"],
      ["📅", "dob", fmtDate(id.date_of_birth), "date_of_birth"],
      ["📍", "city", id.birth_city, "birth_city"],
      ["🌍", "nationality", id.nationality],
      ["🪪", "fan", v.fan],
      ["🏦", "type", v.account_type],
    ];
    const list = $("#reviewList"); list.innerHTML = "";
    rows.forEach(([ico, key, val, field]) => {
      const row = document.createElement("div");
      const flag = field && v.mismatches.includes(field) ? `<span class="flag">⚠ ${L("mismatch")}</span>` : "";
      row.innerHTML = `<span>${ico}</span><dt>${L(key)}</dt><dd></dd>`;
      row.querySelector("dd").textContent = val || "—";
      if (flag) row.querySelector("dd").insertAdjacentHTML("beforeend", flag);
      list.append(row);
    });
    const warn = $("#reviewWarn"); warn.hidden = !v.mismatches.length; warn.textContent = L("mismatchNote");
  }
  async function reviewAction(action) {
    const data = await call("/api/review", signed({ action }));
    if (!data) return;
    render();
    if (action === "edit") say(data.reply);
  }

  // ------------------------------------------------------------------ creation + success
  async function runCreation() {
    show("creating"); journey("creating");
    const list = $("#progress"); list.innerHTML = "";
    const items = L("progress").map((t) => { const li = document.createElement("li"); li.textContent = t; list.append(li); return li; });
    const wait = (ms) => new Promise((r) => setTimeout(r, ms));
    const req = api("/api/account/create", signed());
    for (const li of items) { li.classList.add("busy"); await wait(850); li.classList.replace("busy", "ok"); }
    try {
      const data = await req;
      S.state = data.state; S.token = data.token; S.view = data.view; S.extra = data.extra;
      render();
    } catch (e) { toast(e.message); }
  }
  function showDone() {
    show("done"); journey("done");
    $("#acctNo").textContent = S.extra.account_number;
    $("#acctType").textContent = S.extra.account_type;
    if (S.stream) stopCamera();
    clearInterval(S.timer);
  }
  function download() {
    const v = S.view, id = v.identity || {};
    const lines = [
      "DASHEN BANK – ACCOUNT DETAILS", "=".repeat(32),
      `Account Holder : ${id.full_name}`, `Account Number : ${S.extra.account_number}`,
      `Account Type   : ${S.extra.account_type}`, `Date of Birth  : ${id.date_of_birth}`,
      `Birth City     : ${id.birth_city}`, `Nationality    : ${id.nationality}`,
      `FAN            : ${v.fan}`, `Opened         : ${new Date().toLocaleString()}`,
      "", "Opened via the Dashen Bank AI Video Assistant (demo).",
    ];
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([lines.join("\n")], { type: "text/plain" }));
    a.download = `dashen-account-${S.extra.account_number.replace(/\s/g, "")}.txt`;
    a.click(); URL.revokeObjectURL(a.href);
  }

  // ------------------------------------------------------------------ wiring
  function init() {
    applyI18n();
    $$(".lang-toggle button").forEach((b) => b.addEventListener("click", () => { S.lang = b.dataset.lang; applyI18n(); }));
    $("#btnCreate").addEventListener("click", beginCall);
    $("#btnPromo").addEventListener("click", beginCall);
    $$(".demo-only").forEach((b) => b.addEventListener("click", () => toast(L("demoOnly"))));
    $$("[data-back]").forEach((b) => b.addEventListener("click", () => { if (confirm(L("endCall"))) goHome(); }));
    $("#ccEnd").addEventListener("click", () => { if (confirm(L("endCall"))) goHome(); });
    $("#ccMute").addEventListener("click", (e) => { S.muted = !S.muted; e.currentTarget.textContent = S.muted ? "🔇" : "🔊"; if (S.muted && "speechSynthesis" in window) speechSynthesis.cancel(); });
    $("#ccCam").addEventListener("click", () => (S.stream ? stopCamera() : startCamera()));
    $("#ccCaptions").addEventListener("click", (e) => { S.captions = !S.captions; e.currentTarget.classList.toggle("off", !S.captions); $("#bubble").classList.toggle("hidden", !S.captions); });

    $("#btnStart").addEventListener("click", () => sendMessage(S.lang === "am" ? "አዎ" : "Yes, let's get started"));
    $("#btnMic").addEventListener("click", listen);
    $$("[data-speak]").forEach((b) => b.addEventListener("click", listen));
    $("#formText").addEventListener("submit", (e) => { e.preventDefault(); sendMessage($("#inText").value.trim()); });
    $("#formDate").addEventListener("submit", (e) => { e.preventDefault(); sendMessage($("#inDate").value); });
    $("#formChoice").addEventListener("submit", (e) => { e.preventDefault(); sendMessage($("#inChoice").value.trim()); });
    $("#inFan").addEventListener("input", (e) => { const d = e.target.value.replace(/\D/g, "").slice(0, 12); e.target.value = d.replace(/(\d{4})(?=\d)/g, "$1 "); });
    $("#formFan").addEventListener("submit", (e) => { e.preventDefault(); sendMessage($("#inFan").value); });

    wireOtpBoxes();
    $("#formOtp").addEventListener("submit", verifyOtp);
    $("#btnResend").addEventListener("click", async () => {
      const data = await call("/api/otp/resend", signed());
      if (data) { showOtp(); toast(data.reply); }
    });
    $("#btnEdit").addEventListener("click", () => reviewAction("edit"));
    $("#btnConfirm").addEventListener("click", () => reviewAction("confirm"));
    $("#btnCopy").addEventListener("click", () => navigator.clipboard?.writeText(S.extra.account_number.replace(/\s/g, "")).then(() => toast(L("copied"))));
    $("#btnDownload").addEventListener("click", download);
    $("#btnMyAccount").addEventListener("click", goHome);

    if ("speechSynthesis" in window) speechSynthesis.onvoiceschanged = () => {};
    fetch("/api/health").then((r) => r.json()).then((h) => {
      $("#llmMode").textContent = h.llm === "none" ? "LLM: rule-based mode (set ANTHROPIC_API_KEY or OPENAI_API_KEY to enable the LLM)" : `LLM: ${h.llm} via LangChain`;
    }).catch(() => {});
    journey("home");
  }
  init();
})();
