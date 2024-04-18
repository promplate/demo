<script>
  import { TokenSquare } from "@promplate/pattern";
  import { onMount } from "svelte";
  import { sineInOut } from "svelte/easing";
  import { tweened } from "svelte/motion";

  const length = 20;
  let i = tweened(length * 1.3, { easing: sineInOut, duration: 700 });

  onMount(() => ($i = 0));
</script>

<div class="grid h-screen select-none place-items-center bg-neutral-950">
  <div class="flex flex-col gap-2 text-neutral-2">
    <div class="text-sm">
      <TokenSquare {length} isHighlighted={({ x, y }) => y - x >= $i} />
    </div>
    <h1 class="mx-0.5 w-fit text-white font-sans">
      Promplate
      <span class="op-30">Demo</span>
    </h1>
  </div>
</div>
