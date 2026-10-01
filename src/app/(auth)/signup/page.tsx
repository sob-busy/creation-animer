import type { Metadata } from "next";
import Link from "next/link";

import { AuthHeader } from "../auth-header";
import { SignupForm } from "./signup-form";

export const metadata: Metadata = { title: "Créer un compte" };

export default function SignupPage() {
  return (
    <>
      <AuthHeader title="Créez votre studio" description="Gratuit pour démarrer. Aucune carte requise." />
      <SignupForm />
      <p className="mt-8 text-center text-sm text-muted-foreground">
        Déjà inscrit ?{" "}
        <Link href="/login" className="font-medium text-foreground underline-offset-4 hover:underline">
          Se connecter
        </Link>
      </p>
    </>
  );
}
