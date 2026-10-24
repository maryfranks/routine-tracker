import { useEffect, useState, type ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { CADENCES, type Cadence } from "@/lib/periods";
import { cn } from "@/lib/utils";

interface Props {
  trigger: ReactNode;
  initial?: { name: string; cadence: Cadence };
  onSubmit: (v: { name: string; cadence: Cadence }) => Promise<unknown>;
}

export function ViewDialog({ trigger, initial, onSubmit }: Props) {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [cadence, setCadence] = useState<Cadence>("daily");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (open) {
      setName(initial?.name ?? "");
      setCadence(initial?.cadence ?? "daily");
    }
  }, [open, initial?.name, initial?.cadence]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    try {
      await onSubmit({ name, cadence });
      setOpen(false);
    } catch {
      /* toast shown by mutation */
    } finally {
      setBusy(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent>
        <form onSubmit={submit} className="space-y-5">
          <DialogHeader>
            <DialogTitle className="font-display text-3xl font-normal">{initial ? "Edit view" : "New view"}</DialogTitle>
            <DialogDescription>Every task in a view repeats on the view's cadence.</DialogDescription>
          </DialogHeader>
          <div className="space-y-2">
            <Label htmlFor="view-name">Name</Label>
            <Input id="view-name" autoFocus value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Health" maxLength={80} />
          </div>
          <div className="space-y-2">
            <Label>Cadence</Label>
            <div className="grid grid-cols-3 gap-2" role="radiogroup">
              {CADENCES.map((c) => (
                <button
                  type="button"
                  role="radio"
                  aria-checked={cadence === c.value}
                  key={c.value}
                  onClick={() => setCadence(c.value)}
                  className={cn(
                    "rounded-md border px-3 py-3 text-left text-sm transition-colors",
                    cadence === c.value ? "border-primary bg-accent text-accent-foreground" : "hover:bg-muted",
                  )}
                >
                  <div className="font-medium">{c.label}</div>
                  <div className="text-xs text-muted-foreground">Once per {c.noun}</div>
                </button>
              ))}
            </div>
            {initial && initial.cadence !== cadence && (
              <p className="text-xs text-muted-foreground">Changing cadence starts fresh periods; past records stay in history under the old cadence only while it matches.</p>
            )}
          </div>
          <DialogFooter>
            <Button type="button" variant="ghost" onClick={() => setOpen(false)}>Cancel</Button>
            <Button type="submit" disabled={busy || !name.trim()}>{busy ? "Saving…" : initial ? "Save" : "Create view"}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
