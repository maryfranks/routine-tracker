import { type Cadence } from "@/lib/periods";

export interface User {
  id: string;
  email: string;
  createdAt: string;
}

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

export interface ClockOffset {
  days: number;
  weeks: number;
  months: number;
}

export interface ClockState {
  now: string;
  simulated: boolean;
  offset: ClockOffset;
}

export interface HistoryTask {
  id: string;
  title: string;
  done: boolean;
}

export interface HistoryPeriod {
  key: string;
  start: string;
  tasks: HistoryTask[];
}

export interface ViewHistory {
  view: View;
  periods: HistoryPeriod[];
}

export class ApiError extends Error {}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let message = "An error occurred";
    try {
      const data = await res.json();
      if (typeof data.detail === "string") {
        message = data.detail;
      } else if (Array.isArray(data.detail)) {
        message = data.detail.map((err: any) => err.msg || JSON.stringify(err)).join(", ");
      } else if (data.message) {
        message = data.message;
      }
    } catch {
      message = res.statusText || message;
    }
    throw new ApiError(message);
  }
  if (res.status === 204) {
    return {} as T;
  }
  return res.json();
}

export const api = {
  // Authentication
  async register(input: { email: string; password: string }): Promise<User> {
    const res = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(input),
    });
    return handleResponse<User>(res);
  },

  async login(input: { email: string; password: string }): Promise<User> {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(input),
    });
    return handleResponse<User>(res);
  },

  async logout(): Promise<void> {
    const res = await fetch("/api/auth/logout", {
      method: "POST",
      credentials: "include",
    });
    return handleResponse<void>(res);
  },

  async getCurrentUser(): Promise<User> {
    const res = await fetch("/api/auth/me", {
      credentials: "include",
    });
    return handleResponse<User>(res);
  },

  // Clock
  async getClock(): Promise<ClockState> {
    const res = await fetch("/api/clock", {
      credentials: "include",
    });
    return handleResponse<ClockState>(res);
  },

  async advanceClock(unit: "day" | "week" | "month"): Promise<ClockState> {
    const res = await fetch("/api/clock/advance", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ unit }),
    });
    return handleResponse<ClockState>(res);
  },

  async resetClock(): Promise<ClockState> {
    const res = await fetch("/api/clock/reset", {
      method: "POST",
      credentials: "include",
    });
    return handleResponse<ClockState>(res);
  },

  // Views
  async listViews(): Promise<(View & { taskCount: number; doneCount: number })[]> {
    const res = await fetch("/api/views", {
      credentials: "include",
    });
    return handleResponse<(View & { taskCount: number; doneCount: number })[]>(res);
  },

  async createView(input: { name: string; cadence: Cadence }): Promise<View> {
    const res = await fetch("/api/views", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(input),
    });
    return handleResponse<View>(res);
  },

  async updateView(id: string, input: { name: string; cadence: Cadence }): Promise<View> {
    const res = await fetch(`/api/views/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(input),
    });
    return handleResponse<View>(res);
  },

  async deleteView(id: string): Promise<void> {
    const res = await fetch(`/api/views/${id}`, {
      method: "DELETE",
      credentials: "include",
    });
    return handleResponse<void>(res);
  },

  // Tasks
  async listTasks(viewId: string): Promise<TaskWithStatus[]> {
    const res = await fetch(`/api/views/${viewId}/tasks`, {
      credentials: "include",
    });
    return handleResponse<TaskWithStatus[]>(res);
  },

  async createTask(viewId: string, title: string): Promise<Task> {
    const res = await fetch(`/api/views/${viewId}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ title }),
    });
    return handleResponse<Task>(res);
  },

  async updateTask(id: string, title: string): Promise<Task> {
    const res = await fetch(`/api/tasks/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ title }),
    });
    return handleResponse<Task>(res);
  },

  async deleteTask(id: string): Promise<void> {
    const res = await fetch(`/api/tasks/${id}`, {
      method: "DELETE",
      credentials: "include",
    });
    return handleResponse<void>(res);
  },

  async setTaskDone(id: string, done: boolean): Promise<void> {
    const res = await fetch(`/api/tasks/${id}/done`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ done }),
    });
    return handleResponse<void>(res);
  },

  // History
  async getHistory(): Promise<ViewHistory[]> {
    const res = await fetch("/api/history", {
      credentials: "include",
    });
    return handleResponse<ViewHistory[]>(res);
  },

  // Utilities
  async loadDemoData(): Promise<void> {
    const res = await fetch("/api/demo", {
      method: "POST",
      credentials: "include",
    });
    return handleResponse<void>(res);
  },

  async resetToEmpty(): Promise<void> {
    const res = await fetch("/api/reset", {
      method: "POST",
      credentials: "include",
    });
    return handleResponse<void>(res);
  },
};
