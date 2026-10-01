"use client";

import { useActionState } from "react";

import { FormAlert } from "@/components/forms/form-alert";
import { FormField } from "@/components/forms/form-field";
import { SubmitButton } from "@/components/forms/submit-button";
import type { FormState } from "@/lib/validations/form";

import { requestPasswordReset } from "../actions";

export function ForgotForm() {
  const [state, action] = useActionState<FormState, FormData>(requestPasswordReset, {});

  if (state.success) return <FormAlert type="success" message={state.success} />;

  return (
    <form action={action} className="grid gap-5" noValidate>
      <FormAlert type="error" message={state.error} />
      <FormField
        name="email"
        type="email"
        label="E-mail"
        autoComplete="email"
        required
        errors={state.fieldErrors?.email}
      />
      <SubmitButton pendingLabel="Envoi…">Envoyer le lien</SubmitButton>
    </form>
  );
}
