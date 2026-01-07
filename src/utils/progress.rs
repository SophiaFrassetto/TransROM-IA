use indicatif::{ProgressBar, ProgressStyle};
use std::time::Instant;

pub fn timed_bar<T>(total: u64, msg: &'static str, f: impl FnOnce(&ProgressBar) -> T) -> T {
    let pb = ProgressBar::new(total);
    pb.set_style(
        ProgressStyle::with_template(
            "{msg:20} [{bar:30.magenta/black}] {percent:>3}% {pos:>8}/{len:<8} {prefix:>8}",
        )
        .unwrap()
        .progress_chars("█▉▊▋▌▍▎▏ "),
    );
    pb.set_message(msg);

    let start = Instant::now();
    let out = f(&pb);

    let elapsed = start.elapsed().as_millis();
    pb.set_prefix(format!("{elapsed}ms"));

    pb.finish();
    out
}
