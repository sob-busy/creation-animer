import type { Metadata } from "next";
import Link from "next/link";

import { AuthHeader } from "../auth-header";
import { ForgotForm } from "./forgot-form";

export const metadata: Metadata = { title: "Mot de passe oublié" };

export default function ForgotPasswordPage() {
  return (
    <>
      <AuthHeader
        title="Mot de passe oublié"
        description="Saisissez votre e-mail, nous vous enverrons un lien de réinitialisation."
      />
      <ForgotForm />
      <p className="mt-8 text-center text-sm text-muted-foreground">
        <Link href="/login" className="font-medium text-foreground underline-offset-4 hover:underline">
          Retour à la connexion
        </Link>
      </p>
    </>
  );
}
