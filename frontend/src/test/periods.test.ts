import { describe, expect, it } from "vitest";
import { pastPeriods, periodKey } from "@/lib/periods";

describe("periods", () => {
  it("weeks start on Monday", () => {
    expect(periodKey(new Date(2026, 9, 25), "weekly")).toBe("w:2026-10-19"); // Sunday
    expect(periodKey(new Date(2026, 9, 26), "weekly")).toBe("w:2026-10-26"); // Monday
  });
  it("a new day is a new daily period (no rollover)", () => {
    expect(periodKey(new Date(2026, 9, 24, 23), "daily")).not.toBe(periodKey(new Date(2026, 9, 25, 0), "daily"));
  });
  it("monthly keys group by calendar month", () => {
    expect(periodKey(new Date(2026, 9, 1), "monthly")).toBe(periodKey(new Date(2026, 9, 31), "monthly"));
  });
  it("past periods exclude the current one", () => {
    const p = pastPeriods(new Date(2026, 9, 20), new Date(2026, 9, 24), "daily");
    expect(p.length).toBe(4);
  });
});
