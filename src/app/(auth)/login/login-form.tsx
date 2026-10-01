"use client";

import Link from "next/link";
import { useActionState } from "react";

import { FormAlert } from "@/components/forms/form-alert";
import { FormField } from "@/components/forms/form-field";
import { SubmitButton } from "@/components/forms/submit-button";
import type { FormState } from "@/lib/validations/form";

import { signIn } from "../actions";

export function LoginForm({ next, notice }: { next?: string; notice?: string }) {
  const [state, action] = useActionState<FormState, FormData>(signIn, {});

  return (
    <form action={action} className="grid gap-5" noValidate>
      <FormAlert type="error" message={state.error ?? notice} />
      <input type="hidden" name="next" value={next ?? "/dashboard"} />
      <FormField
        name="email"
        type="email"
        label="E-mail"
        autoComplete="email"
        placeholder="vous@atelier.com"
        required
        errors={state.fieldErrors?.email}
      />
      <div className="grid gap-2">
        <FormField
          name="password"
          type="password"
          label="Mot de passe"
          autoComplete="current-password"
          required
          errors={state.fieldErrors?.password}
        />
        <Link
          href="/forgot-password"
          className="justify-self-end text-xs text-muted-foreground underline-offset-4 hover:text-foreground hover:underline"
        >
          Mot de passe oublié ?
        </Link>
      </div>
      <SubmitButton pendingLabel="Connexion…">Se connecter</SubmitButton>
    </form>
  );
}
