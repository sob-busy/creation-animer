"use client";

import { useActionState, useEffect } from "react";
import { toast } from "sonner";

import { FormAlert } from "@/components/forms/form-alert";
import { FormField } from "@/components/forms/form-field";
import { SubmitButton } from "@/components/forms/submit-button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { MEASUREMENTS } from "@/lib/validations/client";
import type { FormState } from "@/lib/validations/form";

export type ClientDefaults = Record<string, string | undefined>;

export function ClientForm({
  action,
  defaults = {},
  submitLabel,
}: {
  action: (prev: FormState, formData: FormData) => Promise<FormState>;
  defaults?: ClientDefaults;
  submitLabel: string;
}) {
  const [state, formAction] = useActionState<FormState, FormData>(action, {});
  const v = (name: string) => state.values?.[name] ?? defaults[name];
  const err = (name: string) => state.fieldErrors?.[name];

  useEffect(() => {
    if (state.success) toast.success(state.success);
  }, [state]);

  return (
    <form action={formAction} className="grid gap-6" noValidate>
      <FormAlert type="error" message={state.error} />

      <Card>
        <CardHeader>
          <CardTitle>Identité</CardTitle>
          <CardDescription>Coordonnées utilisées pour les rendez-vous et les factures.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-5 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <FormField name="fullName" label="Nom complet" autoComplete="off" required defaultValue={v("fullName")} errors={err("fullName")} />
          </div>
          <FormField name="email" type="email" label="E-mail" autoComplete="off" defaultValue={v("email")} errors={err("email")} />
          <FormField name="phone" type="tel" label="Téléphone" autoComplete="off" placeholder="+221 77 000 00 00" defaultValue={v("phone")} errors={err("phone")} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Mesures</CardTitle>
          <CardDescription>En centimètres. Laissez vide ce qui n&apos;a pas encore été pris.</CardDescription>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-5 md:grid-cols-3">
          {MEASUREMENTS.map(({ key, label }) => (
            <FormField
              key={key}
              name={`m_${key}`}
              label={label}
              inputMode="decimal"
              placeholder="—"
              defaultValue={v(`m_${key}`)}
              errors={err(`m_${key}`)}
            />
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Notes</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-2">
          <Label htmlFor="notes" className="sr-only">
            Notes
          </Label>
          <Textarea id="notes" name="notes" rows={4} placeholder="Préférences, tissus, morphologie…" defaultValue={v("notes")} aria-invalid={Boolean(err("notes")) || undefined} />
          {err("notes") && <p className="text-xs font-medium text-destructive">{err("notes")![0]}</p>}
        </CardContent>
      </Card>

      <div className="sm:ml-auto sm:w-56">
        <SubmitButton pendingLabel="Enregistrement…">{submitLabel}</SubmitButton>
      </div>
    </form>
  );
}
