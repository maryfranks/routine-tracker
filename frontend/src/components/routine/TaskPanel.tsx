import { useState } from "react";
import { Check, ListTodo, Pencil, Plus, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAction, useClock, useTasks } from "@/hooks/use-routine";
import { api, type TaskWithStatus, type View } from "@/services/api";
import { currentPeriodName, formatResetsIn, periodLabel } from "@/lib/periods";
import { cn } from "@/lib/utils";
import { EmptyState, ErrorState, ListSkeleton } from "./states";

export function TaskPanel({ view }: { view: View }) {
  const tasks = useTasks(view.id);
  const clock = useClock();
  const [title, setTitle] = useState("");
  const add = useAction((t: string) => api.createTask(view.id, t));
  const now = clock.data ? new Date(clock.data.now) : null;

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      await add.mutateAsync(title);
      setTitle("");
    } catch { /* toasted */ }
  }

  const doneCount = tasks.data?.filter((t) => t.done).length ?? 0;

  return (
    <section className="space-y-5">
      <div>
        <p className="text-xs uppercase tracking-widest text-muted-foreground">
          {currentPeriodName(view.cadence)}{now && ` · ${periodLabel(now, view.cadence)}`}
        </p>
        <div className="mt-1 flex items-baseline justify-between gap-3">
          <h1 className="font-display text-5xl">{view.name}</h1>
          {tasks.data && tasks.data.length > 0 && (
            <span className="text-sm text-muted-foreground">{doneCount} of {tasks.data.length} done</span>
          )}
        </div>
        {now && <p className="mt-1 text-sm text-muted-foreground">{formatResetsIn(now, view.cadence)}. Unfinished tasks simply start fresh.</p>}
      </div>

      <form onSubmit={submit} className="flex gap-2">
        <Input value={title} onChange={(e) => setTitle(e.target.value)} placeholder={`Add a ${view.cadence} task…`} maxLength={80} aria-label="New task" />
        <Button type="submit" disabled={add.isPending || !title.trim()}><Plus className="size-4" />Add</Button>
      </form>

      {tasks.isPending ? (
        <ListSkeleton />
      ) : tasks.isError ? (
        <ErrorState error={tasks.error} onRetry={() => tasks.refetch()} />
      ) : tasks.data.length === 0 ? (
        <EmptyState icon={<ListTodo className="size-7" />} title="No tasks yet">
          Add something you want to do once per {view.cadence === "daily" ? "day" : view.cadence === "weekly" ? "week" : "month"}.
        </EmptyState>
      ) : (
        <ul className="divide-y rounded-lg border bg-card">
          {tasks.data.map((t) => <TaskRow key={t.id} task={t} />)}
        </ul>
      )}
    </section>
  );
}

function TaskRow({ task }: { task: TaskWithStatus }) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [optimistic, setOptimistic] = useState<boolean | null>(null);
  const toggle = useAction((d: boolean) => api.setTaskDone(task.id, d));
  const rename = useAction((t: string) => api.updateTask(task.id, t));
  const remove = useAction(() => api.deleteTask(task.id), "Task deleted");
  const done = optimistic ?? task.done;

  function flip() {
    setOptimistic(!done);
    toggle.mutate(!done, { onSettled: () => setOptimistic(null) });
  }

  async function save(e: React.FormEvent) {
    e.preventDefault();
    try {
      await rename.mutateAsync(title);
      setEditing(false);
    } catch { /* toasted */ }
  }

  return (
    <li className="group flex items-center gap-3 px-4 py-3">
      <button
        onClick={flip}
        aria-label={done ? `Mark "${task.title}" not done` : `Mark "${task.title}" done`}
        aria-pressed={done}
        className={cn(
          "flex size-6 shrink-0 items-center justify-center rounded-full border-2 transition-colors",
          done ? "border-primary bg-primary text-primary-foreground" : "border-border hover:border-primary",
        )}
      >
        {done && <Check className="size-3.5" strokeWidth={3} />}
      </button>
      {editing ? (
        <form onSubmit={save} className="flex flex-1 gap-2">
          <Input autoFocus value={title} onChange={(e) => setTitle(e.target.value)} maxLength={80} className="h-8" onKeyDown={(e) => e.key === "Escape" && setEditing(false)} />
          <Button size="sm" type="submit" disabled={rename.isPending}>Save</Button>
          <Button size="sm" type="button" variant="ghost" onClick={() => { setTitle(task.title); setEditing(false); }}>Cancel</Button>
        </form>
      ) : (
        <>
          <span className={cn("flex-1 transition-colors", done && "text-muted-foreground line-through")}>{task.title}</span>
          <div className="flex opacity-0 transition-opacity group-focus-within:opacity-100 group-hover:opacity-100">
            <Button variant="ghost" size="icon" className="size-8" aria-label="Rename task" onClick={() => setEditing(true)}><Pencil className="size-3.5" /></Button>
            <Button variant="ghost" size="icon" className="size-8 text-destructive" aria-label="Delete task" disabled={remove.isPending} onClick={() => remove.mutate(undefined)}><Trash2 className="size-3.5" /></Button>
          </div>
        </>
      )}
    </li>
  );
}
