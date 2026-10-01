import { requireUser } from "@/lib/auth";

export default async function DashboardPage() {
  const user = await requireUser();
  return <main className="p-8">Bienvenue, {user.email}</main>;
}
