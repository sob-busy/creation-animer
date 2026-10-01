import type { Metadata } from "next";
import { redirect } from "next/navigation";

import { createClient } from "@/lib/supabase/server";

import { AuthHeader } from "../auth-header";
import { ResetForm } from "./reset-form";

export const metadata: Metadata = { title: "Nouveau mot de passe" };

export default async function ResetPasswordPage() {
  // Only reachable with the temporary session created by the recovery link.
  const supabase = await createClient();
  const { data } = await supabase.auth.getClaims();
  if (!data?.claims) redirect("/forgot-password");

  return (
    <>
      <AuthHeader title="Nouveau mot de passe" description="Choisissez un mot de passe que vous n'utilisez nulle part ailleurs." />
      <ResetForm />
    </>
  );
}
