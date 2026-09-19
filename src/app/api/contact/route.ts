import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const body = await request.json();
  const { name, email, phone } = body ?? {};

  if (!name || !email || !phone) {
    return NextResponse.json({ error: "Missing required fields" }, { status: 400 });
  }

  // TODO: wire this up to your CRM/GoHighLevel or email provider.
  console.log("New quote request:", body);

  return NextResponse.json({ ok: true });
}
