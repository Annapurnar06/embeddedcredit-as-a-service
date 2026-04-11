import { Container } from "@/components/ui/container";

const footerLinks = {
  Platform: [
    { label: "How It Works", href: "#how-it-works" },
    { label: "Tool Stack", href: "#tools" },
    { label: "38 Segments", href: "#segments" },
    { label: "Compliance", href: "#compliance" },
  ],
  "Use Cases": [
    { label: "Dairy Farmer", href: "#use-cases" },
    { label: "Kirana Shop", href: "#use-cases" },
    { label: "Gig Worker", href: "#use-cases" },
    { label: "Gold Loan", href: "#use-cases" },
  ],
  Company: [
    { label: "About", href: "#" },
    { label: "Blog", href: "#" },
    { label: "Careers", href: "#" },
    { label: "Contact", href: "#" },
  ],
  Legal: [
    { label: "Privacy Policy", href: "#" },
    { label: "Terms of Service", href: "#" },
    { label: "RBI Compliance", href: "#compliance" },
  ],
};

export function Footer() {
  return (
    <footer className="bg-secondary text-secondary-foreground">
      <Container>
        <div className="py-16">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-8">
            <div className="col-span-2 md:col-span-1">
              <div className="flex items-center gap-2 mb-4">
                <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
                  <span className="text-white font-bold text-sm">EC</span>
                </div>
                <span className="font-semibold text-white">EmbeddedCredit</span>
              </div>
              <p className="text-sm text-slate-400 leading-relaxed">
                AI-native lending infrastructure for India&apos;s 300 million underserved borrowers.
              </p>
            </div>

            {Object.entries(footerLinks).map(([category, links]) => (
              <div key={category}>
                <h4 className="text-sm font-semibold text-white mb-4">{category}</h4>
                <ul className="space-y-2.5">
                  {links.map((link) => (
                    <li key={link.label}>
                      <a
                        href={link.href}
                        className="text-sm text-slate-400 hover:text-white transition-colors"
                      >
                        {link.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <div className="mt-12 pt-8 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-sm text-slate-500">
              &copy; {new Date().getFullYear()} EmbeddedCredit. All rights reserved.
            </p>
            <p className="text-sm text-slate-500">
              Built for the 300 million.
            </p>
          </div>
        </div>
      </Container>
    </footer>
  );
}
