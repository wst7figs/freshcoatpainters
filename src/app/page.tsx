import Link from "next/link";

const services = [
  {
    title: "Interior Painting",
    desc: "Walls, ceilings, trim, and cabinetry finished with precision and zero mess left behind.",
  },
  {
    title: "Exterior Painting",
    desc: "Weather-resistant coatings that protect your home and boost curb appeal for years.",
  },
  {
    title: "Cabinet Refinishing",
    desc: "Transform tired cabinets into a showroom-quality finish at a fraction of replacement cost.",
  },
  {
    title: "Commercial Painting",
    desc: "Minimal-disruption painting for offices, retail spaces, and multi-unit properties.",
  },
];

const steps = [
  { title: "Free Estimate", desc: "Tell us about your project and get a no-obligation quote within 24 hours." },
  { title: "We Prep & Protect", desc: "Furniture covered, surfaces prepped, and your property treated with care." },
  { title: "Flawless Finish", desc: "Premium paints applied by pros, with a final walkthrough to confirm you love it." },
];

const testimonials = [
  {
    quote:
      "They transformed our entire exterior in two days. Clean, professional, and the color match was perfect.",
    name: "Sarah M.",
  },
  {
    quote:
      "Best painting crew we've hired. On time, respectful of our home, and the cabinets look brand new.",
    name: "David R.",
  },
  {
    quote:
      "Got three quotes, Fresh Coat was the most thorough and the work showed it. Highly recommend.",
    name: "Jennifer T.",
  },
];

export default function Home() {
  return (
    <div>
      <section className="bg-gradient-to-b from-brand-dark to-brand text-white">
        <div className="mx-auto grid max-w-6xl items-center gap-10 px-6 py-20 md:grid-cols-2 md:py-28">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-accent">
              Licensed &amp; Insured
            </p>
            <h1 className="mt-3 text-4xl font-bold leading-tight sm:text-5xl">
              A Fresh Coat Makes All the Difference
            </h1>
            <p className="mt-5 max-w-lg text-lg text-blue-100">
              Professional interior and exterior painting for homes and
              businesses. Quality craftsmanship, on-time completion, and a
              finish you&apos;ll love &mdash; guaranteed.
            </p>
            <div className="mt-8 flex flex-col gap-4 sm:flex-row">
              <Link
                href="/contact"
                className="rounded-full bg-accent px-7 py-3.5 text-center text-sm font-semibold text-brand-dark transition-colors hover:bg-white"
              >
                Get Your Free Estimate
              </Link>
              <a
                href="tel:+15551234567"
                className="rounded-full border border-white/40 px-7 py-3.5 text-center text-sm font-semibold text-white transition-colors hover:bg-white/10"
              >
                Call (555) 123-4567
              </a>
            </div>
          </div>
          <div className="rounded-2xl bg-white/10 p-8 backdrop-blur">
            <dl className="grid grid-cols-2 gap-6 text-center">
              <div>
                <dt className="text-3xl font-bold text-accent">15+</dt>
                <dd className="mt-1 text-sm text-blue-100">Years in Business</dd>
              </div>
              <div>
                <dt className="text-3xl font-bold text-accent">2,000+</dt>
                <dd className="mt-1 text-sm text-blue-100">Homes Painted</dd>
              </div>
              <div>
                <dt className="text-3xl font-bold text-accent">4.9&#9733;</dt>
                <dd className="mt-1 text-sm text-blue-100">Average Rating</dd>
              </div>
              <div>
                <dt className="text-3xl font-bold text-accent">100%</dt>
                <dd className="mt-1 text-sm text-blue-100">Satisfaction Guarantee</dd>
              </div>
            </dl>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-20">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-zinc-900">Our Services</h2>
          <p className="mt-3 text-zinc-600">
            Full-service painting solutions, tailored to your property.
          </p>
        </div>
        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {services.map((s) => (
            <div
              key={s.title}
              className="rounded-xl border border-zinc-200 p-6 transition-shadow hover:shadow-lg"
            >
              <div className="mb-4 h-10 w-10 rounded-lg bg-brand/10" />
              <h3 className="text-lg font-semibold text-zinc-900">{s.title}</h3>
              <p className="mt-2 text-sm text-zinc-600">{s.desc}</p>
            </div>
          ))}
        </div>
        <div className="mt-10 text-center">
          <Link href="/services" className="text-sm font-semibold text-brand hover:text-brand-dark">
            View all services &rarr;
          </Link>
        </div>
      </section>

      <section className="bg-zinc-50 py-20">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-zinc-900">How It Works</h2>
            <p className="mt-3 text-zinc-600">Three simple steps to a beautiful finish.</p>
          </div>
          <div className="mt-12 grid gap-8 md:grid-cols-3">
            {steps.map((step, i) => (
              <div key={step.title} className="text-center">
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-brand text-lg font-bold text-white">
                  {i + 1}
                </div>
                <h3 className="mt-4 text-lg font-semibold text-zinc-900">{step.title}</h3>
                <p className="mt-2 text-sm text-zinc-600">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-20">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-zinc-900">What Our Customers Say</h2>
        </div>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {testimonials.map((t) => (
            <div key={t.name} className="rounded-xl border border-zinc-200 p-6">
              <p className="text-accent">&#9733;&#9733;&#9733;&#9733;&#9733;</p>
              <p className="mt-3 text-sm text-zinc-700">&ldquo;{t.quote}&rdquo;</p>
              <p className="mt-4 text-sm font-semibold text-zinc-900">{t.name}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-brand-dark py-16 text-white">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="text-3xl font-bold">Ready for Your Fresh Coat?</h2>
          <p className="mt-3 text-blue-100">
            Get a free, no-obligation estimate today. Most quotes turned around within 24 hours.
          </p>
          <Link
            href="/contact"
            className="mt-8 inline-block rounded-full bg-accent px-8 py-3.5 text-sm font-semibold text-brand-dark transition-colors hover:bg-white"
          >
            Request Free Estimate
          </Link>
        </div>
      </section>
    </div>
  );
}
