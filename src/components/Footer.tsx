import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-black/5 bg-zinc-50">
      <div className="mx-auto grid max-w-6xl gap-10 px-6 py-14 sm:grid-cols-2 md:grid-cols-4">
        <div>
          <div className="flex items-center gap-2 text-lg font-bold text-brand-dark">
            <span className="inline-block h-3 w-3 rounded-full bg-accent" />
            Fresh Coat Painters
          </div>
          <p className="mt-3 text-sm text-zinc-600">
            Licensed & insured painting contractors delivering flawless
            interior and exterior finishes.
          </p>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-zinc-900">Services</h3>
          <ul className="mt-3 space-y-2 text-sm text-zinc-600">
            <li>Interior Painting</li>
            <li>Exterior Painting</li>
            <li>Cabinet Refinishing</li>
            <li>Commercial Painting</li>
          </ul>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-zinc-900">Company</h3>
          <ul className="mt-3 space-y-2 text-sm">
            <li>
              <Link href="/about" className="text-zinc-600 hover:text-brand">
                About Us
              </Link>
            </li>
            <li>
              <Link href="/gallery" className="text-zinc-600 hover:text-brand">
                Gallery
              </Link>
            </li>
            <li>
              <Link href="/contact" className="text-zinc-600 hover:text-brand">
                Contact
              </Link>
            </li>
          </ul>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-zinc-900">Contact</h3>
          <ul className="mt-3 space-y-2 text-sm text-zinc-600">
            <li>
              <a href="tel:+15551234567" className="hover:text-brand">
                (555) 123-4567
              </a>
            </li>
            <li>
              <a href="mailto:info@freshcoatpainters.com" className="hover:text-brand">
                info@freshcoatpainters.com
              </a>
            </li>
            <li>Mon&ndash;Sat: 7am&ndash;6pm</li>
          </ul>
        </div>
      </div>
      <div className="border-t border-black/5 py-6 text-center text-xs text-zinc-500">
        &copy; {new Date().getFullYear()} Fresh Coat Painters. All rights reserved.
      </div>
    </footer>
  );
}
