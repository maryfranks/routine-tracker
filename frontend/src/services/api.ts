/**
 * Mock API service layer. All data access goes through this module.
 * Every function is async and returns plain JSON-shaped objects, so it can be
 * swapped for a REST client (fetch with `credentials: "include"`) without
 * touching UI components.
 */
import { type Cadence, pastPeriods, periodKey, startOfPeriod } from "@/lib/periods";

export interface View {
  id: string;
  name: string;
  cadence: Cadence;
  createdAt: string;
}
export interface Task {
  id: string;
  viewId: string;
  title: string;
  createdAt: string;
}
export interface TaskWithStatus extends Task {
  done: boolean;
}
export interface Completion {
  taskId: string;
  periodKey: string;
  completedAt: string;
}
export interface ClockOffset {
  days: number;
  months: number;
}
export interface ClockState {
  now: string;
  simulated: boolean;
  offset: ClockOffset;
}
export interface HistoryPeriod {
  key: string;
  start: string;
  tasks: { id: string; title: string; done: boolean }[];
}
export interface ViewHistory {
  view: View;
  periods: HistoryPeriod[];
}

interface Db {
  views: View[];
  tasks: Task[];
  completions: Completion[];
  clock: ClockOffset;
}

const KEY = "routine.db.v1";

export class ApiError extends Error {}

const delay = (min = 120, max = 380) =>
  new Promise((r) => setTimeout(r, min + Math.random() * (max - min)));

const uid = () => Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4);

function emptyDb(clock: ClockOffset = { days: 0, months: 0 }): Db {
  return { views: [], tasks: [], completions: [], clock };
}

function read(): Db {
  if (typeof window === "undefined") return emptyDb();
  const raw = window.localStorage.getItem(KEY);
  if (!raw) {
    const db = buildDemoDb({ days: 0, months: 0 });
    write(db);
    return db;
  }
  try {
    return JSON.parse(raw) as Db;
  } catch {
    throw new ApiError("Stored data is corrupted. Reset data from the developer menu.");
  }
}
function write(db: Db) {
  window.localStorage.setItem(KEY, JSON.stringify(db));
}

export function nowFrom(offset: ClockOffset, live = new Date()): Date {
  const d = new Date(live);
  d.setMonth(d.getMonth() + offset.months);
  d.setDate(d.getDate() + offset.days);
  return d;
}

function hash(s: string) {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return Math.abs(h % 100);
}

function buildDemoDb(clock: ClockOffset): Db {
  const now = nowFrom(clock);
  const ago = (days: number) => new Date(now.getTime() - days * 86_400_000).toISOString();
  const spec: { name: string; cadence: Cadence; age: number; tasks: string[]; rate: number }[] = [
    { name: "Health", cadence: "daily", age: 45, tasks: ["Morning walk", "Stretch 10 min", "Drink 2L water", "Lights out by 11"], rate: 70 },
    { name: "Deep Work", cadence: "daily", age: 30, tasks: ["90-min focus block", "Inbox zero", "Plan tomorrow"], rate: 60 },
    { name: "Home", cadence: "weekly", age: 120, tasks: ["Laundry", "Water plants", "Groceries", "Clean kitchen"], rate: 75 },
    { name: "Finances", cadence: "monthly", age: 300, tasks: ["Review budget", "Pay credit card", "Check subscriptions"], rate: 80 },
  ];
  const db = emptyDb(clock);
  for (const s of spec) {
    const view: View = { id: uid(), name: s.name, cadence: s.cadence, createdAt: ago(s.age) };
    db.views.push(view);
    for (const title of s.tasks) {
      const task: Task = { id: uid(), viewId: view.id, title, createdAt: view.createdAt };
      db.tasks.push(task);
      for (const p of pastPeriods(new Date(view.createdAt), now, s.cadence)) {
        const key = periodKey(p, s.cadence);
        if (hash(title + key) < s.rate)
          db.completions.push({ taskId: task.id, periodKey: key, completedAt: p.toISOString() });
      }
      // a few already done in the current period
      if (hash(title) < 40)
        db.completions.push({ taskId: task.id, periodKey: periodKey(now, s.cadence), completedAt: now.toISOString() });
    }
  }
  return db;
}

function getView(db: Db, id: string) {
  const v = db.views.find((x) => x.id === id);
  if (!v) throw new ApiError("That view no longer exists.");
  return v;
}

const clean = (s: string, label: string) => {
  const t = s.trim();
  if (!t) throw new ApiError(`${label} can't be empty.`);
  if (t.length > 80) throw new ApiError(`${label} must be 80 characters or fewer.`);
  return t;
};

export const api = {
  async getClock(): Promise<ClockState> {
    await delay(40, 80);
    const { clock } = read();
    return { now: nowFrom(clock).toISOString(), simulated: clock.days !== 0 || clock.months !== 0, offset: clock };
  },
  async advanceClock(unit: "day" | "week" | "month"): Promise<void> {
    await delay();
    const db = read();
    if (unit === "day") db.clock.days += 1;
    if (unit === "week") db.clock.days += 7;
    if (unit === "month") db.clock.months += 1;
    write(db);
  },
  async resetClock(): Promise<void> {
    await delay();
    const db = read();
    db.clock = { days: 0, months: 0 };
    write(db);
  },

  async listViews(): Promise<(View & { taskCount: number; doneCount: number })[]> {
    await delay();
    const db = read();
    const now = nowFrom(db.clock);
    return db.views.map((v) => {
      const tasks = db.tasks.filter((t) => t.viewId === v.id);
      const key = periodKey(now, v.cadence);
      const doneCount = tasks.filter((t) => db.completions.some((c) => c.taskId === t.id && c.periodKey === key)).length;
      return { ...v, taskCount: tasks.length, doneCount };
    });
  },
  async createView(input: { name: string; cadence: Cadence }): Promise<View> {
    await delay();
    const db = read();
    const view: View = { id: uid(), name: clean(input.name, "Name"), cadence: input.cadence, createdAt: nowFrom(db.clock).toISOString() };
    db.views.push(view);
    write(db);
    return view;
  },
  async updateView(id: string, input: { name: string; cadence: Cadence }): Promise<View> {
    await delay();
    const db = read();
    const v = getView(db, id);
    v.name = clean(input.name, "Name");
    v.cadence = input.cadence;
    write(db);
    return v;
  },
  async deleteView(id: string): Promise<void> {
    await delay();
    const db = read();
    getView(db, id);
    const taskIds = new Set(db.tasks.filter((t) => t.viewId === id).map((t) => t.id));
    db.views = db.views.filter((v) => v.id !== id);
    db.tasks = db.tasks.filter((t) => !taskIds.has(t.id));
    db.completions = db.completions.filter((c) => !taskIds.has(c.taskId));
    write(db);
  },

  async listTasks(viewId: string): Promise<TaskWithStatus[]> {
    await delay();
    const db = read();
    const view = getView(db, viewId);
    const key = periodKey(nowFrom(db.clock), view.cadence);
    return db.tasks
      .filter((t) => t.viewId === viewId)
      .map((t) => ({ ...t, done: db.completions.some((c) => c.taskId === t.id && c.periodKey === key) }));
  },
  async createTask(viewId: string, title: string): Promise<Task> {
    await delay();
    const db = read();
    getView(db, viewId);
    const task: Task = { id: uid(), viewId, title: clean(title, "Task"), createdAt: nowFrom(db.clock).toISOString() };
    db.tasks.push(task);
    write(db);
    return task;
  },
  async updateTask(id: string, title: string): Promise<void> {
    await delay();
    const db = read();
    const t = db.tasks.find((x) => x.id === id);
    if (!t) throw new ApiError("That task no longer exists.");
    t.title = clean(title, "Task");
    write(db);
  },
  async deleteTask(id: string): Promise<void> {
    await delay();
    const db = read();
    db.tasks = db.tasks.filter((t) => t.id !== id);
    db.completions = db.completions.filter((c) => c.taskId !== id);
    write(db);
  },
  /** Sets completion for the current active period only. */
  async setTaskDone(id: string, done: boolean): Promise<void> {
    await delay(80, 200);
    const db = read();
    const t = db.tasks.find((x) => x.id === id);
    if (!t) throw new ApiError("That task no longer exists.");
    const now = nowFrom(db.clock);
    const key = periodKey(now, getView(db, t.viewId).cadence);
    db.completions = db.completions.filter((c) => !(c.taskId === id && c.periodKey === key));
    if (done) db.completions.push({ taskId: id, periodKey: key, completedAt: now.toISOString() });
    write(db);
  },

  async getHistory(): Promise<ViewHistory[]> {
    await delay(200, 450);
    const db = read();
    const now = nowFrom(db.clock);
    const done = new Set(db.completions.map((c) => `${c.taskId}|${c.periodKey}`));
    return db.views.map((view) => {
      const tasks = db.tasks.filter((t) => t.viewId === view.id);
      const periods = pastPeriods(new Date(view.createdAt), now, view.cadence).map((p) => {
        const key = periodKey(p, view.cadence);
        const end = startOfPeriod(p, view.cadence);
        return {
          key,
          start: p.toISOString(),
          tasks: tasks
            .filter((t) => startOfPeriod(new Date(t.createdAt), view.cadence) <= end)
            .map((t) => ({ id: t.id, title: t.title, done: done.has(`${t.id}|${key}`) })),
        };
      }).filter((p) => p.tasks.length > 0);
      return { view, periods };
    });
  },

  async loadDemoData(): Promise<void> {
    await delay(300, 600);
    write(buildDemoDb({ days: 0, months: 0 }));
  },
  async resetToEmpty(): Promise<void> {
    await delay(300, 600);
    write(emptyDb());
  },
};
