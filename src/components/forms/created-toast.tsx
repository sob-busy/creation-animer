"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { toast } from "sonner";

/** Shows a one-off toast after a create-redirect, then cleans the ?created flag from the URL. */
export function CreatedToast({ message }: { message: string }) {
  const router = useRouter();
  const pathname = usePathname();
  useEffect(() => {
    toast.success(message);
    router.replace(pathname, { scroll: false });
  }, [message, pathname, router]);
  return null;
}
