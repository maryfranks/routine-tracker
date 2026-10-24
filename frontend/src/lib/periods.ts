export type Cadence = "daily" | "weekly" | "monthly";

export const CADENCES: { value: Cadence; label: string; noun: string }[] = [
  { value: "daily", label: "Daily", noun: "day" },
  { value: "weekly", label: "Weekly", noun: "week" },
  { value: "monthly", label: "Monthly", noun: "month" },
];

const pad = (n: number) => String(n).padStart(2, "0");
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

/** Start of the period containing `d`. Weeks start on Monday. */
export function startOfPeriod(d: Date, c: Cadence): Date {
  const x = new Date(d.getFullYear(), d.getMonth(), d.getDate());
  if (c === "weekly") x.setDate(x.getDate() - ((x.getDay() + 6) % 7));
  if (c === "monthly") x.setDate(1);
  return x;
}

export function shiftPeriod(start: Date, c: Cadence, n: number): Date {
  const x = new Date(start);
  if (c === "daily") x.setDate(x.getDate() + n);
  else if (c === "weekly") x.setDate(x.getDate() + 7 * n);
  else x.setMonth(x.getMonth() + n);
  return x;
}

/** Stable key for a period; includes cadence so changing a view's cadence never mixes records. */
export function periodKey(d: Date, c: Cadence): string {
  const s = startOfPeriod(d, c);
  const ym = `${s.getFullYear()}-${pad(s.getMonth() + 1)}`;
  return `${c[0]}:${c === "monthly" ? ym : `${ym}-${pad(s.getDate())}`}`;
}

export function periodLabel(d: Date, c: Cadence): string {
  const s = startOfPeriod(d, c);
  if (c === "daily") return `${DAYS[s.getDay()]}, ${MONTHS[s.getMonth()]} ${s.getDate()}, ${s.getFullYear()}`;
  if (c === "monthly") return `${MONTHS[s.getMonth()]} ${s.getFullYear()}`;
  const e = shiftPeriod(s, "daily", 6);
  return `${MONTHS[s.getMonth()]} ${s.getDate()} – ${MONTHS[e.getMonth()]} ${e.getDate()}, ${e.getFullYear()}`;
}

export function currentPeriodName(c: Cadence): string {
  return c === "daily" ? "Today" : c === "weekly" ? "This week" : "This month";
}

/** Past (completed) periods, newest first, from `now` back to the period containing `since`. */
export function pastPeriods(since: Date, now: Date, c: Cadence, limit = 60): Date[] {
  const floor = startOfPeriod(since, c).getTime();
  const out: Date[] = [];
  let p = shiftPeriod(startOfPeriod(now, c), c, -1);
  while (p.getTime() >= floor && out.length < limit) {
    out.push(p);
    p = shiftPeriod(p, c, -1);
  }
  return out;
}

export function formatResetsIn(now: Date, c: Cadence): string {
  const next = shiftPeriod(startOfPeriod(now, c), c, 1);
  const days = Math.ceil((next.getTime() - now.getTime()) / 86_400_000);
  if (days <= 1) return "Resets at midnight";
  return `Resets in ${days} days`;
}
