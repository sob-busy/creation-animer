import { z } from "zod";

const email = z
  .string({ required_error: "L'e-mail est requis." })
  .trim()
  .toLowerCase()
  .max(254, "E-mail trop long.")
  .email("Adresse e-mail invalide.");

const password = z
  .string({ required_error: "Le mot de passe est requis." })
  .min(8, "8 caractères minimum.")
  .max(72, "72 caractères maximum.") // bcrypt limit used by Supabase Auth
  .regex(/[a-zA-Z]/, "Au moins une lettre.")
  .regex(/[0-9]/, "Au moins un chiffre.");

export const signInSchema = z.object({
  email,
  password: z.string().min(1, "Le mot de passe est requis.").max(72),
});

export const signUpSchema = z.object({
  fullName: z
    .string()
    .trim()
    .min(2, "2 caractères minimum.")
    .max(100, "100 caractères maximum.")
    .regex(/^[\p{L}\p{M}' .-]+$/u, "Caractères non autorisés."),
  email,
  password,
});

export const forgotPasswordSchema = z.object({ email });

export const resetPasswordSchema = z
  .object({ password, confirmPassword: z.string() })
  .refine((d) => d.password === d.confirmPassword, {
    message: "Les mots de passe ne correspondent pas.",
    path: ["confirmPassword"],
  });

/**
 * Only allow same-site relative redirects ("/dashboard/x"), never "//evil.com"
 * or "https://evil.com" — prevents open-redirect attacks via ?next=.
 */
export function safeRedirectPath(value: unknown, fallback = "/dashboard"): string {
  if (typeof value !== "string") return fallback;
  if (!value.startsWith("/") || value.startsWith("//") || value.startsWith("/\\")) return fallback;
  return value;
}
