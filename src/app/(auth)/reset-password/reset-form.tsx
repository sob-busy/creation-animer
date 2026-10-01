"use client";

import { useActionState } from "react";

import { FormAlert } from "@/components/forms/form-alert";
import { FormField } from "@/components/forms/form-field";
import { SubmitButton } from "@/components/forms/submit-button";
import type { FormState } from "@/lib/validations/form";

import { updatePassword } from "../actions";

export function ResetForm() {
  const [state, action] = useActionState<FormState, FormData>(updatePassword, {});

  return (
    <form action={action} className="grid gap-5" noValidate>
      <FormAlert type="error" message={state.error} />
      <FormField
        name="password"
        type="password"
        label="Nouveau mot de passe"
        autoComplete="new-password"
        hint="8 caractères minimum, avec au moins une lettre et un chiffre."
        required
        errors={state.fieldErrors?.password}
      />
      <FormField
        name="confirmPassword"
        type="password"
        label="Confirmation"
        autoComplete="new-password"
        required
        errors={state.fieldErrors?.confirmPassword}
      />
      <SubmitButton pendingLabel="Enregistrement…">Mettre à jour</SubmitButton>
    </form>
  );
}
