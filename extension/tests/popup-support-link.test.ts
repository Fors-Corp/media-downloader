import { describe, expect, it } from "vitest";
import html from "../src/popup.html?raw";

const doc = new DOMParser().parseFromString(html, "text/html");

describe("popup support link", () => {
  const link = doc.getElementById("mdlx-support-link") as HTMLAnchorElement | null;

  it("is a real, keyboard-reachable anchor to the support page", () => {
    expect(link).not.toBeNull();
    expect(link?.tagName).toBe("A");
    expect(link?.getAttribute("href")).toBe("https://marcfors.com/donate?from=media-downloader");
    expect(link?.hasAttribute("tabindex")).toBe(false);
  });

  it("opens in a new tab without leaking the opener", () => {
    expect(link?.getAttribute("target")).toBe("_blank");
    expect(link?.getAttribute("rel")).toBe("noopener noreferrer");
  });

  it("has a meaningful accessible name", () => {
    expect(link?.textContent?.trim()).toBe("Support · 1,99 €");
  });
});
