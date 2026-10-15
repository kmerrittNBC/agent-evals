**Yes—plan an Angular update, but this doesn’t look like an emergency for this repo as configured.**

`financial-hq-ui/package.json` pins `@angular/router` at **22.1.7**, below the fix for the recent Router advisory, **22.2.0**. That advisory describes a high-severity denial of service, but requires **server-side rendering (SSR) on Node.js/V8**. The repo’s app build targets use browser entry points and deploy static SPAs; I found no Angular SSR setup. That makes the advisory’s stated attack path appear inapplicable to the apps in this repo.

There’s also an Angular SSR open-redirect advisory fixed in **22.2.1**. To cover both, target **22.2.1 or later** on the 22.x line, keeping the Angular packages aligned. I’d schedule that for the next normal maintenance release and test the apps; **raise it to urgent** if any deployment or downstream consumer actually renders these apps with Angular SSR.

Sources: [Router DoS advisory](https://github.com/angular/angular/security/advisories/GHSA-ff3f-86qr-9cv3) · [SSR open-redirect advisory](https://github.com/angular/angular/security/advisories/GHSA-w739-gvwx-grc3).
