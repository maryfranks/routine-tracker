import type { ReactNode } from "react";
import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

export function ErrorState({ error, onRetry }: { error: unknown; onRetry: () => void }) {
  const message = error instanceof Error ? error.message : "Something went wrong.";
  const isAuthError = message.toLowerCase().includes("unauthorized") || message.toLowerCase().includes("not authenticated") || message.toLowerCase().includes("401");

  return (
    <div role="alert" className="flex flex-col items-center gap-3 rounded-lg border border-destructive/30 bg-destructive/5 px-6 py-10 text-center">
      <AlertCircle className="size-6 text-destructive" />
      <p className="font-medium">Couldn't load this</p>
      <p className="max-w-sm text-sm text-muted-foreground">{message}</p>
      <div className="flex gap-2">
        {isAuthError ? (
          <Button asChild size="sm">
            <a href="/login">Sign in</a>
          </Button>
        ) : (
          <Button variant="outline" size="sm" onClick={onRetry}>Try again</Button>
        )}
      </div>
    </div>
  );
}

export function EmptyState({ icon, title, children, action }: { icon: ReactNode; title: string; children?: ReactNode; action?: ReactNode }) {
  return (
    <div className="flex flex-col items-center gap-3 rounded-lg border border-dashed px-6 py-14 text-center">
      <div className="text-muted-foreground">{icon}</div>
      <h2 className="font-display text-3xl">{title}</h2>
      {children && <div className="max-w-md text-sm text-muted-foreground">{children}</div>}
      {action && <div className="mt-2">{action}</div>}
    </div>
  );
}

export function ListSkeleton({ rows = 4 }: { rows?: number }) {
  return (
    <div className="space-y-2" aria-label="Loading">
      {Array.from({ length: rows }, (_, i) => <Skeleton key={i} className="h-12 w-full" />)}
    </div>
  );
}
