import type { Metadata } from "next";
import PageHero from "@/components/PageHero";
import ContactForm from "@/components/ContactForm";

export const metadata: Metadata = {
  title: "Contact | Fresh Coat Painters",
  description: "Request your free painting estimate from Fresh Coat Painters today.",
};

export default function ContactPage() {
  return (
    <div>
      <PageHero
        title="Get Your Free Estimate"
        subtitle="Tell us about your project and we'll get back to you within 24 hours."
      />
      <section className="mx-auto max-w-5xl px-6 py-16">
        <div className="grid gap-12 md:grid-cols-2">
          <div>
            <h2 className="text-xl font-bold text-zinc-900">Contact Details</h2>
            <ul className="mt-4 space-y-3 text-sm text-zinc-600">
              <li>
                <span className="font-medium text-zinc-900">Phone:</span>{" "}
                <a href="tel:+15551234567" className="hover:text-brand">
                  (555) 123-4567
                </a>
              </li>
              <li>
                <span className="font-medium text-zinc-900">Email:</span>{" "}
                <a href="mailto:info@freshcoatpainters.com" className="hover:text-brand">
                  info@freshcoatpainters.com
                </a>
              </li>
              <li>
                <span className="font-medium text-zinc-900">Hours:</span> Mon&ndash;Sat, 7am&ndash;6pm
              </li>
              <li>
                <span className="font-medium text-zinc-900">Service Area:</span> Greater metro area &amp; surrounding suburbs
              </li>
            </ul>
          </div>
          <div className="rounded-xl border border-zinc-200 p-6">
            <ContactForm />
          </div>
        </div>
      </section>
    </div>
  );
}
