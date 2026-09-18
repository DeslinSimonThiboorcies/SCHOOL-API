import { useState } from "react";
import { ArrowRight, CalendarDays, GraduationCap, LockKeyhole, Mail, Phone, UserRound } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { register } from "../services/api";

function Login() {
  const { login } = useAuth();
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ full_name: "", email: "", phone_number: "", date_of_birth: "", password: "" });
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function updateField(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);
    try {
      if (mode === "login") {
        await login({ email: form.email, password: form.password });
      } else {
        await register({ ...form, phone_number: form.phone_number || null, role: "STUDENT" });
        await login({ email: form.email, password: form.password });
      }
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-panel">
        <div className="auth-brand"><span className="brand-mark"><GraduationCap size={22} /></span><span><strong>Northstar</strong><small>Academy operations</small></span></div>
        <div className="auth-copy"><p className="eyebrow">School workspace</p><h1>{mode === "login" ? "Welcome back." : "Create your account."}</h1><p>{mode === "login" ? "Sign in to manage your school operations from one secure workspace." : "Join the school workspace and keep your academic information in one place."}</p></div>
        <form className="login-form" onSubmit={handleSubmit}>
          {mode === "register" && <label><span>Full name</span><div className="input-shell"><UserRound size={17} /><input name="full_name" value={form.full_name} onChange={updateField} placeholder="Your full name" required /></div></label>}
          <label><span>Email address</span><div className="input-shell"><Mail size={17} /><input name="email" type="email" value={form.email} onChange={updateField} placeholder="you@school.edu" required /></div></label>
          {mode === "register" && <><label><span>Date of birth</span><div className="input-shell"><CalendarDays size={17} /><input name="date_of_birth" type="date" value={form.date_of_birth} onChange={updateField} required /></div></label><label><span>Phone number <small>(optional)</small></span><div className="input-shell"><Phone size={17} /><input name="phone_number" type="tel" value={form.phone_number} onChange={updateField} placeholder="Your phone number" /></div></label></>}
          <label><span>Password</span><div className="input-shell"><LockKeyhole size={17} /><input name="password" type="password" minLength="8" value={form.password} onChange={updateField} placeholder="At least 8 characters" required /></div></label>
          {error && <p className="form-error" role="alert">{error}</p>}
          <button className="primary-button login-button" type="submit" disabled={isSubmitting}>{isSubmitting ? (mode === "login" ? "Signing in..." : "Creating account...") : (mode === "login" ? "Sign in" : "Create account")}<ArrowRight size={17} /></button>
        </form>
        <button className="auth-switch" type="button" onClick={() => { setMode(mode === "login" ? "register" : "login"); setError(""); }}>{mode === "login" ? "New here? Create an account" : "Already have an account? Sign in"}</button>
        <p className="auth-footnote">Your account is created securely in the school system</p>
      </section>
      <aside className="auth-aside"><span className="aside-kicker">One clear view</span><h2>Make every school day easier to run.</h2><p>Bring people, attendance, academics, and finance into a calm operational rhythm.</p><div className="aside-rule" /><span>Northstar Academy · 2026</span></aside>
    </main>
  );
}

export default Login;