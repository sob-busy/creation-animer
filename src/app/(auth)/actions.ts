"use server";

import { headers } from "next/headers";
import { redirect } from "next/navigation";

import { publicEnv } from "@/lib/env/client";
import { createClient } from "@/lib/supabase/server";
import {
  forgotPasswordSchema,
  resetPasswordSchema,
  safeRedirectPath,
  signInSchema,
  signUpSchema,
} from "@/lib/validations/auth";
import { echoValues, parseForm, type FormState } from "@/lib/validations/form";

async function siteUrl() {
  // Prefer the configured URL; never trust the Host header for e-mail links in production.
  const configured = process.env.NEXT_PUBLIC_SITE_URL;
  if (configured) return publicEnv().NEXT_PUBLIC_SITE_URL;
  const h = await headers();
  return `${h.get("x-forwarded-proto") ?? "http"}://${h.get("host")}`;
}

export async function signIn(_prev: FormState, formData: FormData): Promise<FormState> {
  const parsed = parseForm(signInSchema, formData);
  if (!parsed.data) return parsed.state;

  const supabase = await createClient();
  const { error } = await supabase.auth.signInWithPassword(parsed.data);
  if (error) {
    // Generic message: do not reveal whether the account exists.
    return { error: "E-mail ou mot de passe incorrect.", values: echoValues(Object.fromEntries(formData)) };
  }
  redirect(safeRedirectPath(formData.get("next")));
}

export async function signUp(_prev: FormState, formData: FormData): Promise<FormState> {
  const parsed = parseForm(signUpSchema, formData);
  if (!parsed.data) return parsed.state;

  const supabase = await createClient();
  const { error } = await supabase.auth.signUp({
    email: parsed.data.email,
    password: parsed.data.password,
    options: {
      data: { full_name: parsed.data.fullName },
      emailRedirectTo: `${await siteUrl()}/auth/confirm?next=/dashboard`,
    },
  });
  if (error && error.code !== "user_already_exists") {
    const values = echoValues(Object.fromEntries(formData));
    if (error.code === "weak_password") return { error: "Mot de passe trop faible ou compromis.", values };
    if (error.status === 429) return { error: "Trop de tentatives, réessayez dans quelques minutes.", values };
    return { error: "Inscription impossible pour le moment.", values };
  }
  // Same answer whether or not the e-mail already exists (anti-enumeration).
  return { success: "Vérifiez votre boîte mail pour confirmer votre compte." };
}

export async function requestPasswordReset(_prev: FormState, formData: FormData): Promise<FormState> {
  const parsed = parseForm(forgotPasswordSchema, formData);
  if (!parsed.data) return parsed.state;

  const supabase = await createClient();
  await supabase.auth.resetPasswordForEmail(parsed.data.email, {
    redirectTo: `${await siteUrl()}/auth/confirm?next=/reset-password`,
  });
  return { success: "Si un compte existe pour cet e-mail, un lien de réinitialisation vient d'être envoyé." };
}

export async function updatePassword(_prev: FormState, formData: FormData): Promise<FormState> {
  const parsed = parseForm(resetPasswordSchema, formData);
  if (!parsed.data) return parsed.state;

  const supabase = await createClient();
  const { data } = await supabase.auth.getClaims();
  if (!data?.claims) return { error: "Lien expiré. Recommencez la procédure." };

  const { error } = await supabase.auth.updateUser({ password: parsed.data.password });
  if (error) {
    if (error.code === "same_password") return { error: "Choisissez un mot de passe différent de l'ancien." };
    return { error: "Impossible de mettre à jour le mot de passe." };
  }
  redirect("/dashboard");
}

export async function signOut() {
  const supabase = await createClient();
  await supabase.auth.signOut();
  redirect("/login");
}
