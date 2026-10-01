import type { z } from "zod";

export type FormState = {
  error?: string;
  success?: string;
  fieldErrors?: Record<string, string[] | undefined>;
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
    } satisfies FormState,
  };
}
