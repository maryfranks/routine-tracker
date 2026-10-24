import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { api } from "@/services/api";

export const keys = {
  clock: ["clock"] as const,
  views: ["views"] as const,
  tasks: (viewId: string) => ["tasks", viewId] as const,
  history: ["history"] as const,
};

export const useClock = () => useQuery({ queryKey: keys.clock, queryFn: api.getClock });
export const useViews = () => useQuery({ queryKey: keys.views, queryFn: api.listViews });
export const useTasks = (viewId: string) =>
  useQuery({ queryKey: keys.tasks(viewId), queryFn: () => api.listTasks(viewId) });
export const useHistory = () => useQuery({ queryKey: keys.history, queryFn: api.getHistory });

/** Mutation that invalidates everything on success and toasts errors. */
export function useAction<A, R>(fn: (a: A) => Promise<R>, success?: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: fn,
    onSuccess: () => {
      qc.invalidateQueries();
      if (success) toast.success(success);
    },
    onError: (e) => toast.error(e instanceof Error ? e.message : "Something went wrong"),
  });
}
