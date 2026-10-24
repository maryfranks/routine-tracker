<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.
<!-- LOVABLE:END -->

## Architecture
- All data access goes through `src/services/api.ts` (async, JSON-shaped); UI uses it only via react-query hooks in `src/hooks/use-routine.ts`, so it can be swapped for a REST client.
- Period math (keys, labels, past periods) lives in `src/lib/periods.ts`; completions are keyed by `taskId + periodKey`, so no rollover state is ever stored.
