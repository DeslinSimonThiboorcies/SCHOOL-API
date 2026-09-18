import {
  Bell,
  BookOpen,
  CalendarDays,
  ChevronDown,
  ChevronRight,
  ClipboardCheck,
  GraduationCap,
  LayoutDashboard,
  MoreHorizontal,
  Search,
  Settings,
  Users,
  WalletCards,
} from "lucide-react";
import { useEffect, useState } from "react";
import { checkApiHealth } from "../services/api";
import { useAuth } from "../context/AuthContext";

const attendance = [78, 84, 81, 88, 86, 92, 89];

const schedule = [
  { time: "08:30", subject: "Mathematics", room: "Room 204", type: "Class 8A", color: "blue" },
  { time: "10:15", subject: "World History", room: "Room 112", type: "Class 9B", color: "orange" },
  { time: "12:00", subject: "Biology Lab", room: "Science Lab", type: "Class 10A", color: "green" },
  { time: "14:30", subject: "Faculty meeting", room: "Conference room", type: "Staff", color: "purple" },
];

const payments = [
  { name: "Olivia Bennett", className: "Grade 8A", amount: "$1,250.00", status: "Paid", initials: "OB", color: "coral" },
  { name: "Liam Carter", className: "Grade 9B", amount: "$980.00", status: "Pending", initials: "LC", color: "blue" },
  { name: "Sophia Wilson", className: "Grade 10A", amount: "$1,250.00", status: "Paid", initials: "SW", color: "violet" },
  { name: "Noah Mitchell", className: "Grade 7C", amount: "$760.00", status: "Overdue", initials: "NM", color: "green" },
];

function StatCard({ label, value, detail, icon: Icon, tone }) {
  return (
    <article className="stat-card">
      <div className={`stat-icon ${tone}`}><Icon size={20} strokeWidth={2.2} /></div>
      <div className="stat-copy">
        <span>{label}</span>
        <strong>{value}</strong>
        <small className={detail.startsWith("+") ? "positive" : "muted"}>{detail}</small>
      </div>
      <button className="icon-button subtle" aria-label={`More about ${label}`}><MoreHorizontal size={19} /></button>
    </article>
  );
}

function Home() {
  const { user, logout } = useAuth();
  const [apiStatus, setApiStatus] = useState("checking");

  useEffect(() => {
    checkApiHealth()
      .then(() => setApiStatus("connected"))
      .catch(() => setApiStatus("offline"));
  }, []);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><GraduationCap size={22} /></div>
          <div><strong>Northstar</strong><span>Academy</span></div>
        </div>

        <div className="sidebar-label">Workspace</div>
        <nav className="main-nav" aria-label="Main navigation">
          <a className="nav-item active" href="#dashboard"><LayoutDashboard size={18} /> Dashboard</a>
          <a className="nav-item" href="#students"><Users size={18} /> Students <span className="nav-count">842</span></a>
          <a className="nav-item" href="#academics"><BookOpen size={18} /> Academics</a>
          <a className="nav-item" href="#attendance"><ClipboardCheck size={18} /> Attendance</a>
          <a className="nav-item" href="#calendar"><CalendarDays size={18} /> Calendar</a>
          <a className="nav-item" href="#finance"><WalletCards size={18} /> Finance</a>
        </nav>

        <div className="sidebar-label">Manage</div>
        <nav className="main-nav" aria-label="Management navigation">
          <a className="nav-item" href="#staff"><Users size={18} /> Staff</a>
          <a className="nav-item" href="#settings"><Settings size={18} /> Settings</a>
        </nav>

        <div className="sidebar-footer">
          <div className="help-card"><span className="help-spark">✦</span><strong>Need a hand?</strong><p>Visit the help center for quick answers.</p><button>Open help center <ChevronRight size={14} /></button></div>
          <button className="user-profile" onClick={logout} title="Sign out"><div className="avatar avatar-dark">{user.full_name.slice(0, 2).toUpperCase()}</div><div><strong>{user.full_name}</strong><span>{user.role}</span></div><ChevronDown size={16} /></button>
        </div>
      </aside>

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <div className="breadcrumb"><span>Workspace</span><ChevronRight size={14} /><strong>Overview</strong></div>
          <div className="top-actions">
            <label className="search-box"><Search size={17} /><input aria-label="Search" placeholder="Search anything..." /></label>
            <button className="icon-button notification" aria-label="Notifications"><Bell size={19} /><i /></button>
            <div className="avatar avatar-coral">JD</div>
          </div>
        </header>

        <div className="content-wrap">
          <section className="page-heading">
            <div><p className="eyebrow">Tuesday, September 18, 2026</p><h1>Good morning, {user.full_name.split(" ")[0]} <span>✦</span></h1><p className="heading-copy">Here&apos;s what&apos;s happening across Northstar Academy today.</p><span className={`api-status ${apiStatus}`}><i /> API {apiStatus}</span></div>
            <button className="primary-button"><span>+</span> Add new</button>
          </section>

          <section className="stats-grid" aria-label="School overview">
            <StatCard label="Total students" value="842" detail="+12.5% this month" icon={Users} tone="blue" />
            <StatCard label="Present today" value="92.4%" detail="+3.2% from yesterday" icon={ClipboardCheck} tone="green" />
            <StatCard label="Outstanding fees" value="$24,860" detail="12 invoices pending" icon={WalletCards} tone="orange" />
            <StatCard label="Teaching staff" value="64" detail="2 on leave today" icon={BookOpen} tone="purple" />
          </section>

          <section className="dashboard-grid">
            <article className="panel attendance-panel">
              <div className="panel-heading"><div><h2>Attendance overview</h2><p>Weekly attendance rate across all grades</p></div><button className="select-button">This week <ChevronDown size={15} /></button></div>
              <div className="chart-meta"><strong>87.8%</strong><span className="trend-up">↑ 4.8% <em>vs. last week</em></span></div>
              <div className="chart"><div className="chart-lines"><span>100%</span><span>75%</span><span>50%</span><span>25%</span><span>0%</span></div><div className="chart-area"><div className="chart-fill" /><svg viewBox="0 0 700 190" preserveAspectRatio="none" role="img" aria-label="Attendance trend rising through the week"><path className="chart-line" d="M0,102 C50,90 65,110 110,82 S175,95 225,66 S285,86 335,61 S390,74 445,48 S505,66 555,39 S620,55 700,25" /></svg><div className="chart-dots">{attendance.map((value, index) => <span key={value} style={{ left: `${index * 16.66}%`, bottom: `${(value - 65) * 2.4}%` }} />)}</div></div><div className="chart-days"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div></div>
            </article>

            <article className="panel schedule-panel">
              <div className="panel-heading"><div><h2>Today&apos;s schedule</h2><p>Tuesday, September 18</p></div><button className="round-arrow" aria-label="View calendar"><ChevronRight size={18} /></button></div>
              <div className="schedule-list">{schedule.map((item) => <div className="schedule-item" key={item.time}><time>{item.time}</time><span className={`schedule-dot ${item.color}`} /><div><strong>{item.subject}</strong><p>{item.room}</p></div><span className="class-tag">{item.type}</span></div>)}</div>
              <button className="text-button">View full schedule <ChevronRight size={15} /></button>
            </article>
          </section>

          <section className="lower-grid">
            <article className="panel payments-panel">
              <div className="panel-heading"><div><h2>Recent fee payments</h2><p>Latest transactions from parents and guardians</p></div><button className="text-button">View all <ChevronRight size={15} /></button></div>
              <div className="table-wrap"><table><thead><tr><th>Student</th><th>Amount</th><th>Status</th><th>Date</th><th /></tr></thead><tbody>{payments.map((payment, index) => <tr key={payment.name}><td><div className="student-cell"><div className={`avatar avatar-${payment.color}`}>{payment.initials}</div><div><strong>{payment.name}</strong><span>{payment.className}</span></div></div></td><td className="amount">{payment.amount}</td><td><span className={`status ${payment.status.toLowerCase()}`}>{payment.status}</span></td><td className="date">Sep {18 - index}, 2026</td><td><button className="icon-button subtle" aria-label={`More actions for ${payment.name}`}><MoreHorizontal size={18} /></button></td></tr>)}</tbody></table></div>
            </article>
            <article className="panel updates-panel"><div className="panel-heading"><div><h2>Quick updates</h2><p>What needs your attention</p></div><button className="icon-button subtle" aria-label="More updates"><MoreHorizontal size={19} /></button></div><div className="updates-list"><div className="update-item"><span className="update-icon orange"><WalletCards size={17} /></span><div><strong>12 fee invoices are overdue</strong><p>Review outstanding balances</p></div><ChevronRight size={16} /></div><div className="update-item"><span className="update-icon blue"><Users size={17} /></span><div><strong>3 new enrollment requests</strong><p>Awaiting your approval</p></div><ChevronRight size={16} /></div><div className="update-item"><span className="update-icon green"><CalendarDays size={17} /></span><div><strong>Parent-teacher evening</strong><p>Tomorrow at 5:30 PM</p></div><ChevronRight size={16} /></div></div><button className="outline-button">See all updates</button></article>
          </section>
        </div>
      </main>
    </div>
  );
}

export default Home;