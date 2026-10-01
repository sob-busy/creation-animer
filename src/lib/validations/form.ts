import type { z } from "zod";

export type FormState = {
  error?: string;
  success?: string;
  fieldErrors?: Record<string, string[] | undefined>;
  /** Submitted values echoed back so fields are not wiped on error (never passwords). */
  values?: Record<string, string>;
};

/** Parse FormData against a Zod schema, returning typed data or field errors. */
export function parseForm<S extends z.ZodTypeAny>(schema: S, formData: FormData) {
  const raw = Object.fromEntries(
    [...formData.entries()].filter(([, v]) => typeof v === "string"),
  );
  const result = schema.safeParse(raw);
  if (result.success) return { data: result.data as z.infer<S> };
  return {
    state: {
      error: "Veuillez corriger les champs indiqués.",
      fieldErrors: result.error.flatten().fieldErrors as FormState["fieldErrors"],
      values: echoValues(raw),
    } satisfies FormState,
  };
}

/** Keeps non-sensitive inputs so the form can be re-filled after an error. */
export function echoValues(raw: Record<string, FormDataEntryValue>): Record<string, string> {
  return Object.fromEntries(
    Object.entries(raw).filter(([k, v]) => typeof v === "string" && !/password/i.test(k)),
  ) as Record<string, string>;
}
