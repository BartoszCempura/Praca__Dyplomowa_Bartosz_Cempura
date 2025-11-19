function Footer() {
  return (
    <div className="flex justify-center bg-base-200">
      <footer className="flex justify-around footer sm:footer-horizontal bg-base-200 text-neutral-content p-10 mt-10 shadow-sm w-4/5">
          <nav>
              <h6 className="footer-title text-cyan-500">Services</h6>
              <a className="link link-hover">Branding</a>
              <a className="link link-hover">Design</a>
              <a className="link link-hover">Marketing</a>
              <a className="link link-hover">Advertisement</a>
          </nav>
          <nav>
              <h6 className="footer-title text-cyan-500">Company</h6>
              <a className="link link-hover">About us</a>
              <a className="link link-hover">Contact</a>
              <a className="link link-hover">Jobs</a>
              <a className="link link-hover">Press kit</a>
          </nav>
          <nav>
              <h6 className="footer-title text-cyan-500">Legal</h6>
              <a className="link link-hover">Terms of use</a>
              <a className="link link-hover">Privacy policy</a>
              <a className="link link-hover">Cookie policy</a>
          </nav>
      </footer>
    </div>
  )
}

export default Footer;