import { z } from "zod";

/** Body measurements captured for a client, in centimetres. */
export const MEASUREMENTS = [
  { key: "chest", label: "Poitrine" },
  { key: "waist", label: "Taille" },
  { key: "hips", label: "Hanches" },
  { key: "shoulders", label: "Épaules" },
  { key: "arm", label: "Longueur de bras" },
  { key: "length", label: "Longueur totale" },
] as const;

export type MeasurementKey = (typeof MEASUREMENTS)[number]["key"];

const optionalText = (max: number, message: string) =>
  z
    .string()
    .trim()
    .max(max, message)
    .transform((v) => (v === "" ? null : v));

const measurement = z
  .string()
  .trim()
  .transform((v) => v.replace(",", "."))
  .refine((v) => v === "" || /^\d{1,3}(\.\d)?$/.test(v), "Nombre en cm, 1 décimale max.")
  .transform((v) => (v === "" ? null : Number(v)))
  .refine((v) => v === null || (v > 0 && v <= 300), "Entre 1 et 300 cm.")
  .optional()
  .transform((v) => v ?? null);

export const clientSchema = z.object({
  fullName: z.string().trim().min(1, "Le nom est requis.").max(120, "120 caractères maximum."),
  email: z
    .string()
    .trim()
    .toLowerCase()
    .max(254)
    .refine((v) => v === "" || z.string().email().safeParse(v).success, "Adresse e-mail invalide.")
    .transform((v) => (v === "" ? null : v)),
  phone: z
    .string()
    .trim()
    .max(32, "32 caractères maximum.")
    .refine((v) => v === "" || /^\+?[0-9 ().-]{6,}$/.test(v), "Numéro invalide.")
    .transform((v) => (v === "" ? null : v)),
  notes: optionalText(5000, "5000 caractères maximum."),
  m_chest: measurement,
  m_waist: measurement,
  m_hips: measurement,
  m_shoulders: measurement,
  m_arm: measurement,
  m_length: measurement,
});

export type ClientInput = z.infer<typeof clientSchema>;

/** Map validated input to the DB row shape (measurements as a jsonb object). */
export function toClientRow(input: ClientInput) {
  const measurements: Partial<Record<MeasurementKey, number>> = {};
  for (const { key } of MEASUREMENTS) {
    const v = input[`m_${key}`];
    if (v !== null) measurements[key] = v;
  }
  return { full_name: input.fullName, email: input.email, phone: input.phone, notes: input.notes, measurements };
}

export const uuidSchema = z.string().uuid();
