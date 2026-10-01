import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type Props = React.ComponentProps<typeof Input> & {
  name: string;
  label: string;
  errors?: string[];
  hint?: string;
};

/** Accessible field: label, input, hint and error message wired with aria-*. */
export function FormField({ name, label, errors, hint, id, ...props }: Props) {
  const inputId = id ?? name;
  const errorId = `${inputId}-error`;
  const hintId = `${inputId}-hint`;
  const hasError = Boolean(errors?.length);

  return (
    <div className="grid gap-2">
      <Label htmlFor={inputId}>{label}</Label>
      <Input
        id={inputId}
        name={name}
        aria-invalid={hasError || undefined}
        aria-describedby={[hasError && errorId, hint && hintId].filter(Boolean).join(" ") || undefined}
        {...props}
      />
      {hint && !hasError && (
        <p id={hintId} className="text-xs text-muted-foreground">
          {hint}
        </p>
      )}
      {hasError && (
        <p id={errorId} className="text-xs font-medium text-destructive">
          {errors![0]}
        </p>
      )}
    </div>
  );
}
