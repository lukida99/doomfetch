# Wiring doomfetch into your shell

## On every new terminal

**bash** - in `~/.bashrc`:

```bash
doomfetch -r --no-title
```

**zsh** - in `~/.zshrc`:

```zsh
doomfetch -r --no-title
```

**fish** - in `~/.config/fish/config.fish`:

```fish
if status is-interactive
    doomfetch -r --no-title
end
```

For bash/zsh, guard it so scripts and `scp` do not get a face full of ANSI:

```bash
[[ $- == *i* ]] && doomfetch -r --no-title
```

## Together with fastfetch

See `fastfetch-config.jsonc` next to this file. The short version: set
`logo.type` to `none` and add doomfetch as the first `command` module.

## Together with neofetch

neofetch takes a text file as its logo, so write the output first:

```bash
doomfetch -r --no-title > /tmp/doom-logo
neofetch --ascii /tmp/doom-logo --ascii_colors distro
```

## On SSH login

In `~/.profile` or `/etc/profile.d/doomfetch.sh`:

```bash
command -v doomfetch >/dev/null && doomfetch -r --category monster --no-title
```

## Always the same sprite

```bash
doomfetch -n cacodemon --no-title
```

## A hand-picked random pool

```bash
doomfetch -r --names imp,cacodemon,baron,revenant,cyberdemon --no-title
```
