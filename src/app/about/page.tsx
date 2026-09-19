import type { Metadata } from "next";
import PageHero from "@/components/PageHero";

export const metadata: Metadata = {
  title: "About Us | Fresh Coat Painters",
  description:
    "Learn about Fresh Coat Painters — a licensed, insured painting company with 15+ years serving homeowners and businesses.",
};

const values = [
  {
    title: "Licensed & Insured",
    desc: "Full coverage on every job, so you're protected from start to finish.",
  },
  {
    title: "Quality Materials",
    desc: "We use premium paints built to last, not the cheapest option on the shelf.",
  },
  {
    title: "On-Time, Every Time",
    desc: "We show up when we say we will and finish on schedule.",
  },
  {
    title: "Satisfaction Guarantee",
    desc: "Not happy with a detail? We'll make it right at no extra cost.",
  },
];

export default function AboutPage() {
  return (
    <div>
      <PageHero
        title="About Fresh Coat Painters"
        subtitle="15+ years of trusted, professional painting for homeowners and businesses."
      />
      <section className="mx-auto max-w-4xl px-6 py-16">
        <h2 className="text-2xl font-bold text-zinc-900">Our Story</h2>
        <p className="mt-4 text-zinc-600">
          Fresh Coat Painters started with a simple idea: painting
          contractors should show up on time, communicate clearly, and leave
          your property cleaner than they found it. Over 15 years and 2,000+
          projects later, that&apos;s still how we operate &mdash; whether
          it&apos;s a single accent wall or a full commercial repaint.
        </p>
        <p className="mt-4 text-zinc-600">
          Our crews are trained, background-checked, and treat every home and
          business like it&apos;s their own. From the first estimate to the
          final walkthrough, you&apos;ll always know what&apos;s happening
          and when.
        </p>

        <h2 className="mt-14 text-2xl font-bold text-zinc-900">Why Homeowners Choose Us</h2>
        <div className="mt-6 grid gap-6 sm:grid-cols-2">
          {values.map((v) => (
            <div key={v.title} className="rounded-xl border border-zinc-200 p-6">
              <h3 className="font-semibold text-zinc-900">{v.title}</h3>
              <p className="mt-2 text-sm text-zinc-600">{v.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
