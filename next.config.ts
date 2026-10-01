import type { NextConfig } from "next";

// Guard: anything prefixed NEXT_PUBLIC_ is shipped to the browser. Refuse to build
// if a secret-looking variable was exposed by mistake.
const leaked = Object.keys(process.env).filter(
  (k) => k.startsWith("NEXT_PUBLIC_") && /SERVICE_ROLE|SECRET|PRIVATE|WEBHOOK|SK_/i.test(k),
);
if (leaked.length > 0) {
  throw new Error(`Secret exposé côté client via NEXT_PUBLIC_ : ${leaked.join(", ")}. Retirez le préfixe.`);
}

const isDev = process.env.NODE_ENV !== "production";
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "";
const supabaseWs = supabaseUrl.replace(/^http/, "ws");

// Content-Security-Policy: limits where scripts, styles, images and API calls may come from.
// 'unsafe-inline' for scripts is required by Next.js hydration unless nonces are used
// (nonces force fully dynamic rendering); everything else is locked down.
const csp = [
  "default-src 'self'",
  `script-src 'self' 'unsafe-inline'${isDev ? " 'unsafe-eval'" : ""} https://js.stripe.com`,
  "style-src 'self' 'unsafe-inline'",
  `img-src 'self' data: blob: ${supabaseUrl}`.trim(),
  "font-src 'self' data:",
  `connect-src 'self' ${supabaseUrl} ${supabaseWs} https://api.stripe.com`.trim(),
  "frame-src https://js.stripe.com https://hooks.stripe.com",
  "frame-ancestors 'none'",
  "form-action 'self'",
  "base-uri 'self'",
  "object-src 'none'",
  ...(isDev ? [] : ["upgrade-insecure-requests"]),
].join("; ");

const securityHeaders = [
  { key: "Content-Security-Policy", value: csp },
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(self), microphone=(), geolocation=(), payment=(self)" },
];

const nextConfig: NextConfig = {
  poweredByHeader: false,
  reactStrictMode: true,
  async headers() {
    return [{ source: "/:path*", headers: securityHeaders }];
  },
};

export default nextConfig;
