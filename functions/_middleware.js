// Move fictoepub.pages.dev to fictoepub.yansquared.com with a permanent redirect.
// Preview deployments (<hash>.fictoepub.pages.dev) are left alone, and so are the
// search-engine verification files, so the old property stays verified for Change of Address.
const NEW_ORIGIN = "https://fictoepub.yansquared.com";
const KEEP = new Set(["/google55a4e1cc27afffdf.html", "/google55a4e1cc27afffdf", "/f27e409db1944e348446b6cc2082a2fa.txt", "/BingSiteAuth.xml"]);

export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (url.hostname === "fictoepub.pages.dev" && !KEEP.has(url.pathname) && (request.method === "GET" || request.method === "HEAD")) {
    return new Response(null, { status: 301, headers: { Location: NEW_ORIGIN + url.pathname + url.search, "Cache-Control": "public, max-age=86400" } });
  }
  return next();
}
