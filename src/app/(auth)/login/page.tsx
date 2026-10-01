import type { Metadata } from "next";
import Link from "next/link";

import { safeRedirectPath } from "@/lib/validations/auth";

import { AuthHeader } from "../auth-header";
import { LoginForm } from "./login-form";

export const metadata: Metadata = { title: "Connexion" };

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string; error?: string }>;
}) {
  const { next, error } = await searchParams;
  return (
    <>
      <AuthHeader title="Bon retour" description="Connectez-vous à votre studio StyliZ." />
      <LoginForm
        next={safeRedirectPath(next)}
        notice={error === "link" ? "Ce lien est invalide ou a expiré." : undefined}
      />
      <p className="mt-8 text-center text-sm text-muted-foreground">
        Pas encore de compte ?{" "}
        <Link href="/signup" className="font-medium text-foreground underline-offset-4 hover:underline">
          Créer un studio
        </Link>
      </p>
    </>
  );
}
