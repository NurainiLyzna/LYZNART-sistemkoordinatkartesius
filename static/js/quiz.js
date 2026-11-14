/* Kuis: latihan, pre-test, post-test */
(function () {
  "use strict";
  const form = document.getElementById("quizForm");
  if (!form) return;
  const kind = form.dataset.kind;
  const total = Number(form.dataset.total);
  const answeredEl = document.getElementById("qAnswered");
  const bar = document.getElementById("qBar");
  const timerEl = document.getElementById("qTimer");
  const dialog = document.getElementById("resultDialog");
  const submitBtn = document.getElementById("quizSubmit");
  let graded = false;
  let started = Date.now();

  function answers() {
    const a = {};
    form.querySelectorAll("input[type=radio]:checked").forEach((r) => (a[r.name] = Number(r.value)));
    return a;
  }
  function updateProgress() {
    const n = Object.keys(answers()).length;
    answeredEl.textContent = n;
    bar.style.width = (100 * n / total) + "%";
  }
  form.addEventListener("change", () => { if (!graded) updateProgress(); });

  if (timerEl) {
    setInterval(() => {
      if (graded) return;
      const s = Math.floor((Date.now() - started) / 1000);
      timerEl.textContent = String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0");
    }, 1000);
  }

  function openDialog() {
    if (typeof dialog.showModal === "function") dialog.showModal(); else dialog.setAttribute("open", "");
  }
  function closeDialog() {
    if (typeof dialog.close === "function") dialog.close(); else dialog.removeAttribute("open");
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (graded) return;
    const a = answers();
    const missing = total - Object.keys(a).length;
    if (missing > 0) {
      const first = [...form.querySelectorAll(".question")].find((q) => !q.querySelector("input:checked"));
      if (!confirm(`Masih ada ${missing} soal yang belum dijawab. Tetap kirim jawaban?`)) {
        if (first) first.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      }
    }
    submitBtn.disabled = true;
    submitBtn.textContent = "⏳ Menilai...";
    let r;
    try {
      r = await window.LYZ.api("/api/quiz/" + kind, { answers: a });
    } catch (err) {
      window.LYZ.toast("Gagal mengirim jawaban. Periksa koneksi lalu coba lagi.");
      submitBtn.disabled = false;
      submitBtn.textContent = "✅ Kirim Jawaban";
      return;
    }
    graded = true;
    showFeedback(r);
    showResult(r);
  });

  function showFeedback(r) {
    r.detail.forEach((d) => {
      const fs = document.getElementById(d.id);
      if (!fs) return;
      fs.classList.add(d.given === null ? "q-missing" : d.correct ? "q-correct" : "q-wrong");
      const opts = fs.querySelectorAll(".option");
      opts.forEach((o, i) => {
        o.querySelector("input").disabled = true;
        if (i === d.answer) o.classList.add("is-correct");
        else if (i === d.given) o.classList.add("is-wrong");
      });
      const fb = fs.querySelector(".feedback");
      fb.hidden = false;
      fb.className = "feedback " + (d.correct ? "ok" : "no");
      const head = d.correct ? "✅ Benar!" : d.given === null ? "⚠️ Tidak dijawab." : "❌ Belum tepat.";
      fb.innerHTML = `<b>${head}</b> `;
      fb.appendChild(document.createTextNode("Pembahasan: " + d.explanation));
    });
    submitBtn.hidden = true;
  }

  function showResult(r) {
    const title = document.getElementById("rTitle");
    const msg = r.score >= 90 ? "Luar biasa! 🏆" : r.score >= 75 ? "Hebat! 🎉" : r.score >= 50 ? "Bagus, terus berlatih! 💪" : "Jangan menyerah! 🌱";
    title.textContent = msg;
    document.getElementById("rScore").textContent = r.score;
    document.getElementById("rDetail").textContent = `Benar ${r.correct} dari ${r.total} soal.`;
    const ring = document.getElementById("rRing");
    ring.style.stroke = r.score >= 75 ? "#059669" : r.score >= 50 ? "#7c3aed" : "#f59e0b";
    requestAnimationFrame(() => { ring.style.strokeDashoffset = String(326.7 * (1 - r.score / 100)); });
    const xp = document.getElementById("rXp");
    if (r.saved) xp.textContent = r.xp_gained > 0 ? `+${r.xp_gained} XP ✨` : "Nilai tersimpan. XP diberikan jika kamu melampaui rekor sebelumnya.";
    else xp.textContent = "Masuk/daftar agar nilai dan XP tersimpan.";
    const bd = document.getElementById("rBadges");
    bd.innerHTML = "";
    (r.new_badges || []).forEach((b) => {
      const s = document.createElement("span");
      s.textContent = `${b.icon} ${b.name}`;
      bd.appendChild(s);
    });
    if (r.level) window.LYZ.showRewards({ level: r.level });
    openDialog();
  }

  document.getElementById("rReview").addEventListener("click", () => {
    closeDialog();
    const firstWrong = form.querySelector(".q-wrong, .q-missing") || form.querySelector(".question");
    if (firstWrong) firstWrong.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  document.getElementById("rRetry").addEventListener("click", () => {
    closeDialog();
    graded = false;
    started = Date.now();
    form.reset();
    form.querySelectorAll(".question").forEach((q) => q.classList.remove("q-correct", "q-wrong", "q-missing"));
    form.querySelectorAll(".option").forEach((o) => { o.classList.remove("is-correct", "is-wrong"); o.querySelector("input").disabled = false; });
    form.querySelectorAll(".feedback").forEach((f) => (f.hidden = true));
    submitBtn.hidden = false;
    submitBtn.disabled = false;
    submitBtn.textContent = "✅ Kirim Jawaban";
    updateProgress();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
  dialog.addEventListener("click", (e) => { if (e.target === dialog) closeDialog(); });
})();
