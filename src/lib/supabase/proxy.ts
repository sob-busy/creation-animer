import { NextResponse, type NextRequest } from "next/server";
import { createServerClient } from "@supabase/ssr";

import { publicEnv } from "@/lib/env/client";

/** Routes that require an authenticated user. */
const PROTECTED_PREFIXES = ["/dashboard"];
/** Auth pages a signed-in user should not see again. */
const AUTH_PAGES = ["/login", "/signup", "/forgot-password"];

const matches = (pathname: string, prefixes: string[]) =>
  prefixes.some((p) => pathname === p || pathname.startsWith(`${p}/`));

/**
 * Refreshes the Supabase session cookie and enforces route protection.
 * Uses getClaims(), which verifies the JWT signature — never trust getSession() here.
 */
export async function updateSession(request: NextRequest) {
  let response = NextResponse.next({ request });
  const env = publicEnv();

  const supabase = createServerClient(env.NEXT_PUBLIC_SUPABASE_URL, env.NEXT_PUBLIC_SUPABASE_ANON_KEY, {
    cookies: {
      getAll() {
        return request.cookies.getAll();
      },
      setAll(cookiesToSet, headers) {
        cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value));
        response = NextResponse.next({ request });
        cookiesToSet.forEach(({ name, value, options }) => response.cookies.set(name, value, options));
        Object.entries(headers).forEach(([key, value]) => response.headers.set(key, value));
      },
    },
  });

  // Do not run code between createServerClient and getClaims().
  const { data } = await supabase.auth.getClaims();
  const isAuthenticated = Boolean(data?.claims?.sub);
  const { pathname, search } = request.nextUrl;

  const redirectTo = (path: string) => {
    const url = request.nextUrl.clone();
    url.pathname = path;
    url.search = "";
    if (path === "/login") url.searchParams.set("next", `${pathname}${search}`);
    const redirect = NextResponse.redirect(url);
    // Keep refreshed auth cookies on the redirect response.
    response.cookies.getAll().forEach((c) => redirect.cookies.set(c));
    return redirect;
  };

  if (!isAuthenticated && matches(pathname, PROTECTED_PREFIXES)) return redirectTo("/login");
  if (isAuthenticated && matches(pathname, AUTH_PAGES)) return redirectTo("/dashboard");

  return response;
}
