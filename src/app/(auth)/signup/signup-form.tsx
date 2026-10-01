"use client";

import { useActionState } from "react";

import { FormAlert } from "@/components/forms/form-alert";
import { FormField } from "@/components/forms/form-field";
import { SubmitButton } from "@/components/forms/submit-button";
import type { FormState } from "@/lib/validations/form";

import { signUp } from "../actions";

export function SignupForm() {
  const [state, action] = useActionState<FormState, FormData>(signUp, {});

  if (state.success) return <FormAlert type="success" message={state.success} />;

  return (
    <form action={action} className="grid gap-5" noValidate>
      <FormAlert type="error" message={state.error} />
      <FormField
        name="fullName"
        label="Nom complet"
        autoComplete="name"
        placeholder="Awa Diallo"
        required
        errors={state.fieldErrors?.fullName}
      />
      <FormField
        name="email"
        type="email"
        label="E-mail"
        autoComplete="email"
        placeholder="vous@atelier.com"
        required
        errors={state.fieldErrors?.email}
      />
      <FormField
        name="password"
        type="password"
        label="Mot de passe"
        autoComplete="new-password"
        hint="8 caractères minimum, avec au moins une lettre et un chiffre."
        required
        errors={state.fieldErrors?.password}
      />
      <SubmitButton pendingLabel="Création…">Créer mon studio</SubmitButton>
    </form>
  );
}
