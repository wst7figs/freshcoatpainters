import type { Metadata } from "next";
import Link from "next/link";
import PageHero from "@/components/PageHero";

export const metadata: Metadata = {
  title: "Services | Fresh Coat Painters",
  description:
    "Interior, exterior, cabinet refinishing, and commercial painting services from Fresh Coat Painters.",
};

const services = [
  {
    title: "Interior Painting",
    desc: "From single rooms to whole-home repaints, we protect your floors and furniture and deliver crisp, clean lines every time.",
    bullets: ["Walls & ceilings", "Trim & doors", "Accent walls", "Drywall repair"],
  },
  {
    title: "Exterior Painting",
    desc: "Durable, weather-resistant coatings that hold up against sun, rain, and everything in between.",
    bullets: ["Siding & stucco", "Fascia & trim", "Decks & fences", "Pressure washing prep"],
  },
  {
    title: "Cabinet Refinishing",
    desc: "Get a factory-smooth, showroom finish on your kitchen or bathroom cabinets without the cost of replacement.",
    bullets: ["Sanding & priming", "Spray-finish application", "Hardware removal & reinstall", "Custom color matching"],
  },
  {
    title: "Commercial Painting",
    desc: "Flexible scheduling, including after-hours and weekends, to keep your business running while we work.",
    bullets: ["Offices & retail", "Multi-unit properties", "Low-VOC options", "Project management included"],
  },
];

export default function ServicesPage() {
  return (
    <div>
      <PageHero
        title="Our Services"
        subtitle="Full-service painting for homes and businesses, done right the first time."
      />
      <section className="mx-auto max-w-6xl px-6 py-16">
        <div className="grid gap-10 md:grid-cols-2">
          {services.map((s) => (
            <div key={s.title} className="rounded-xl border border-zinc-200 p-8">
              <h2 className="text-xl font-bold text-zinc-900">{s.title}</h2>
              <p className="mt-3 text-sm text-zinc-600">{s.desc}</p>
              <ul className="mt-4 space-y-2">
                {s.bullets.map((b) => (
                  <li key={b} className="flex items-center gap-2 text-sm text-zinc-700">
                    <span className="h-1.5 w-1.5 rounded-full bg-brand" />
                    {b}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-14 text-center">
          <Link
            href="/contact"
            className="rounded-full bg-brand px-8 py-3.5 text-sm font-semibold text-white transition-colors hover:bg-brand-dark"
          >
            Get a Free Estimate
          </Link>
        </div>
      </section>
    </div>
  );
}
