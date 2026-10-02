/** Currencies offered in the UI (ISO 4217). XOF/XAF first: core market. */
export const CURRENCIES = ["XOF", "XAF", "EUR", "USD", "GBP", "CAD", "MAD", "NGN", "GHS"] as const;
export type Currency = (typeof CURRENCIES)[number];

const decimalsCache = new Map<string, number>();

/** Number of minor-unit digits for a currency (XOF → 0, EUR → 2), from the ICU data. */
export function currencyDecimals(currency: string): number {
  let d = decimalsCache.get(currency);
  if (d === undefined) {
    d = new Intl.NumberFormat("fr-FR", { style: "currency", currency }).resolvedOptions().maximumFractionDigits ?? 2;
    decimalsCache.set(currency, d);
  }
  return d;
}

/** "12,50" / "12.50" (major units) → 1250 (minor units). Returns null if invalid or too precise. */
export function toMinor(input: string, currency: string): number | null {
  const normalized = input.replace(/\s/g, "").replace(",", ".");
  const decimals = currencyDecimals(currency);
  const pattern = decimals === 0 ? /^\d{1,12}$/ : new RegExp(`^\\d{1,12}(\\.\\d{1,${decimals}})?$`);
  if (!pattern.test(normalized)) return null;
  const [whole, frac = ""] = normalized.split(".");
  return Number(whole) * 10 ** decimals + Number(frac.padEnd(decimals, "0") || 0);
}

/** 1250 (minor) + "EUR" → "12,50 €" ; 45000 + "XOF" → "45 000 F CFA". */
export function formatMoney(minor: number, currency: string): string {
  const decimals = currencyDecimals(currency);
  return new Intl.NumberFormat("fr-FR", { style: "currency", currency }).format(minor / 10 ** decimals);
}
