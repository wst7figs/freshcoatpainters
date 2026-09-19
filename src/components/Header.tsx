import Link from "next/link";

const navLinks = [
  { href: "/services", label: "Services" },
  { href: "/gallery", label: "Gallery" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
];

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-black/5 bg-white/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2 text-lg font-bold text-brand-dark">
          <span className="inline-block h-3 w-3 rounded-full bg-accent" />
          Fresh Coat Painters
        </Link>
        <nav className="hidden items-center gap-8 md:flex">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm font-medium text-zinc-700 transition-colors hover:text-brand"
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-4">
          <a
            href="tel:+15551234567"
            className="hidden text-sm font-semibold text-brand-dark sm:block"
          >
            (555) 123-4567
          </a>
          <Link
            href="/contact"
            className="rounded-full bg-brand px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-brand-dark"
          >
            Free Estimate
          </Link>
        </div>
      </div>
    </header>
  );
}
