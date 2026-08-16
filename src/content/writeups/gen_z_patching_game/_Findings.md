Droppinghthe file into pwndbg gives us the following error:

```shell
Reading symbols from Gen_Z_P_Batching_Game.exe...
During symbol reading: Could not find DWO CU /rustc/ded5c06cf21d2b93bffd5d884aa6e96934ee4234\build\x86_64-pc-windows-gnu\stage1-std\x86_64-pc-windows-gnu\release\deps\compiler_builtins-87953880d1763386.compiler_builtins.ace4d55401a4cf31-cgu.145.rcgu.dwo(0x8ca55eda910fa743) referenced by CU at offset 0x104 [in module /mnt/c/Users/Ava Vispilio/Desktop/Snyk-FetchTheFlag/Gen_Z_P_Batching_Game/Gen_Z_P_Batching_Game.exe]
During symbol reading: Could not find DWO CU /rustc/ded5c06cf21d2b93bffd5d884aa6e96934ee4234\build\x86_64-pc-windows-gnu\stage1-std\x86_64-pc-windows-gnu\release\deps\core-6018603b0a83ce5b.core.887804bbdca81d04-cgu.0.rcgu.dwo(0xdb85d1ff859b6f06) referenced by CU at offset 0xd0 [in module /mnt/c/Users/Ava Vispilio/Desktop/Snyk-FetchTheFlag/Gen_Z_P_Batching_Game/Gen_Z_P_Batching_Game.exe]
During symbol reading: Could not find DWO CU /rustc/ded5c06cf21d2b93bffd5d884aa6e96934ee4234\build\x86_64-pc-windows-gnu\stage1-std\x86_64-pc-windows-gnu\release\deps\alloc-3b2e2b2642f765b5.alloc.4dd6f9318cfc53f-cgu.0.rcgu.dwo(0x9598af9f5e20a86a) referenced by CU at offset 0x9c [in module /mnt/c/Users/Ava Vispilio/Desktop/Snyk-FetchTheFlag/Gen_Z_P_Batching_Game/Gen_Z_P_Batching_Game.exe]
During symbol reading: Could not find DWO CU /rustc/ded5c06cf21d2b93bffd5d884aa6e96934ee4234\build\x86_64-pc-windows-gnu\stage1-std\x86_64-pc-windows-gnu\release\deps\memchr-821e20e153e0717f.memchr.62b70d7c59d9367c-cgu.0.rcgu.dwo(0x4d7bf38785907ae9) referenced by CU at offset 0x68 [in module /mnt/c/Users/Ava Vispilio/Desktop/Snyk-FetchTheFlag/Gen_Z_P_Batching_Game/Gen_Z_P_Batching_Game.exe]
During symbol reading: Could not find DWO CU /rustc/ded5c06cf21d2b93bffd5d884aa6e96934ee4234\build\x86_64-pc-windows-gnu\stage1-std\x86_64-pc-windows-gnu\release\deps\panic_unwind-26fcdf10aacc9906.panic_unwind.514cb9de47363daa-cgu.0.rcgu.dwo(0x7b64aab4e9898cce) referenced by CU at offset 0x34 [in module /mnt/c/Users/Ava Vispilio/Desktop/Snyk-FetchTheFlag/Gen_Z_P_Batching_Game/Gen_Z_P_Batching_Game.exe]
During symbol reading: Could not find DWO CU /rustc/ded5c06cf21d2b93bffd5d884aa6e96934ee4234\build\x86_64-pc-windows-gnu\stage1-std\x86_64-pc-windows-gnu\release\deps\std-412f35739dfa5150.std.6f8468120d65d542-cgu.0.rcgu.dwo(0x55beba323fbfa0ac) referenced by CU at offset 0x0 [in module /mnt/c/Users/Ava Vispilio/Desktop/Snyk-FetchTheFlag/Gen_Z_P_Batching_Game/Gen_Z_P_Batching_Game.exe]
```

Long story short, this `.exe` will not run (the long explanation is that is it missing Rust split DWARF debug files - whatever those are...)

Digging around the files shows that:

1.  `__tmainCRTstartup` exists at `0x140001180`
2.  Looking at the Decompiler gives us `main` at `0x1400012ea`
3.  Clicking into `main` shows it lives at `0x14000ba4a`

Nvm, `__main` is literally defined in the `Functions section` - moving on!

Here's what's in `__main`:

```C

/* main::main */

void main::main(void)

{
  longlong lVar1;
  void *pvVar2;
  ulonglong uVar3;
  uint uVar4;
  ulonglong *puVar5;
  undefined8 local_1e0 [6];
  undefined8 local_1b0 [6];
  undefined8 *local_180;
  ulonglong local_178 [3];
  undefined *local_160;
  ulonglong local_158;
  undefined8 uStack_150;
  undefined8 local_148;
  undefined8 uStack_140;
  undefined8 uStack_138;
  undefined8 uStack_130;
  undefined4 local_128;
  undefined4 uStack_124;
  ulonglong local_120;
  undefined8 uStack_118;
  undefined8 local_110;
  undefined4 local_104;
  undefined8 local_100;
  undefined8 uStack_f8;
  undefined8 local_f0;
  undefined8 local_e8 [6];
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  ulonglong local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined1 local_59;
  longlong local_48;
  longlong local_40 [3];
  ulonglong local_28;
  ulonglong *local_20;
  ulonglong *local_18 [3];

  local_59 = 0;
  print_game_banner();
  core::fmt::rt::_<>::new_const(local_1e0,&PTR_s_yo_waddup_brave_adventurer_1400abe08);
  std::io::stdio::_print(local_1e0);
  core::fmt::rt::_<>::new_const(local_1b0,&PTR_s_drop_ur_gamer_tag:_1400abe30);
  std::io::stdio::_print(local_1b0);
  local_180 = std::io::stdio::stdout();
  local_48 = _<>::flush(&local_180);
  if (local_48 != 0) {
    local_40[0] = local_48;
                    /* WARNING: Subroutine does not return */
    core::result::unwrap_failed
              (&DAT_1400aaf38,0x2b,local_40,&PTR_drop_in_place<std::io::error::Error>_1400aaf18,
               &PTR_s_main.rs_1400abe40);
  }
  alloc::string::String::new(local_178);
  local_160 = std::io::stdio::stdin();
  puVar5 = local_178;
  local_28 = std::io::stdio::Stdin::read_line(&local_160,puVar5);
  local_20 = puVar5;
  if ((local_28 & 1) == 0) {
    lVar1 = _<>::deref((longlong)local_178);
    pvVar2 = (void *)core::str::_<impl_str>::trim(lVar1,(ulonglong)puVar5);
    _<>::to_string(&local_120,pvVar2,(ulonglong)puVar5);
    local_104 = 0;
    alloc::vec::Vec<T>::new(&local_100);
    local_59 = 1;
    local_148 = local_110;
    local_158 = local_120;
    uStack_150 = uStack_118;
    uStack_124 = 0;
    local_128 = local_104;
    uStack_130 = local_f0;
    uStack_140 = local_100;
    uStack_138 = uStack_f8;
    core::fmt::rt::Argument::new_display(&local_a8,&local_158);
    local_b8 = local_a8;
    uStack_b0 = uStack_a0;
    uVar4 = 0x400abea0;
    core::fmt::rt::_<>::new_v1(local_e8,&PTR_DAT_1400abea0,&local_b8);
    std::io::stdio::_print(local_e8);
    uVar3 = core::time::Duration::from_millis(0x5dc);
    std::thread::sleep(uVar3,uVar4);
    local_59 = 0;
    local_68 = CONCAT44(uStack_124,local_128);
    local_78 = uStack_138;
    uStack_70 = uStack_130;
    local_88 = local_148;
    uStack_80 = uStack_140;
    local_98 = local_158;
    uStack_90 = uStack_150;
    game_menu((longlong *)&local_98);
    local_59 = 0;
    core::ptr::drop_in_place<>((longlong *)local_178);
    return;
  }
  local_18[0] = puVar5;
                    /* WARNING: Subroutine does not return */
  core::result::unwrap_failed
            (&DAT_1400aaf38,0x2b,local_18,&PTR_drop_in_place<std::io::error::Error>_1400aaf18,
             &PTR_s_main.rs_1400abe58);
}
```

We see `print_game_banner()` and `game_menu()`

In more layman terms, this is what the code is doing:

1. Prints `yo waddup brave adventurer` and `drop ur gamer tag`
2. Creates an empty string for you to input (your gamer tag ig)
3. Creates a player struct:
   ```C
   struct Player {
    name: String,   // offset 0,  size 0x18 (24 bytes)
    scores: Vec<…>, // offset 0x18, size 0x18 (24 bytes)  — or “inventory”, etc.
   }
   ```
4. Prints a welcome message?
5. Sleeps for 1500 ms
6. Calls `game_menu()` with the player struct (`(longlong *)&local_98`)

`game_menu()` is even longer and harder to read. Important details:

- For each of 4 trials, check a byte at param_1+0x31, 0x32, 0x33, 0x34 (actually 0x31 is 49, so that's byte offset)
- The labels are "Glitch Phantom" (Trial 1), "Data Wraith" (Trial 2), "Cipher Demon" (Trial 3), "Sigma Guardian" (Trial 4)
- Print menu options:
  - [5] check ur fragments bestie
  - [6] check ur stats
  - [7] peace out
    "pick a trial no cap:

So we now have a clear direction! Collect fragments from all 4 trials to get our flag!

But first, let's see if we can cheese our `view_fragments()` function to see if the flag has been encoded:

```C

/* main::view_fragments */

void main::view_fragments(longlong param_1)

{
  ulonglong uVar1;
  undefined8 uVar2;
  longlong lVar3;
  undefined **ppuVar4;
  undefined8 local_360 [6];
  undefined8 local_330 [6];
  undefined8 local_300 [6];
  undefined8 local_2d0 [6];
  undefined8 local_2a0 [6];
  undefined8 local_270 [6];
  undefined8 local_240;
  undefined8 local_238;
  undefined8 local_230;
  undefined8 local_228;
  undefined8 local_220;
  undefined8 local_218 [6];
  longlong local_1e8;
  undefined8 local_1e0;
  undefined8 local_1d8;
  undefined *local_1d0 [3];
  longlong local_1b8;
  undefined8 local_1b0;
  undefined8 local_1a8;
  ulonglong local_1a0;
  undefined **local_198;
  undefined **local_190;
  undefined8 local_188 [6];
  ulonglong local_158;
  undefined8 local_150;
  undefined8 local_148;
  undefined8 local_140;
  undefined8 local_138;
  undefined8 local_130;
  undefined8 local_128;
  undefined8 local_120;
  undefined8 local_118;
  undefined8 local_110 [6];
  undefined8 local_e0 [6];
  ulonglong local_b0 [3];
  undefined8 local_98 [6];
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40 [8];

  core::fmt::rt::_<>::new_const(local_360,&PTR_DAT_1400aaff8);
  std::io::stdio::_print(local_360);
  core::fmt::rt::_<>::new_const(local_330,&PTR_DAT_1400ab2c8);
  std::io::stdio::_print(local_330);
  core::fmt::rt::_<>::new_const(local_300,&PTR_DAT_1400ab0e8);
  std::io::stdio::_print(local_300);
  uVar1 = alloc::vec::Vec<T,A>::is_empty(param_1 + 0x18);
  if ((uVar1 & 1) == 0) {
    local_240 = alloc::vec::Vec<T,A>::len(param_1 + 0x18);
    core::fmt::rt::Argument::new_display(&local_228,&local_240);
    local_238 = local_228;
    local_230 = local_220;
    core::fmt::rt::_<>::new_v1(local_270,&PTR_s_Fragments_collected:_1400ab2f0,&local_238);
    std::io::stdio::_print(local_270);
    ppuVar4 = &PTR_DAT_1400ab398;
    core::fmt::rt::_<>::new_const(local_218,&PTR_DAT_1400ab398);
    std::io::stdio::_print(local_218);
    uVar2 = _<>::deref(param_1 + 0x18);
    uVar2 = core::slice::_<impl[T]>::iter(uVar2);
    core::iter::traits::iterator::Iterator::enumerate(local_1d0,uVar2,ppuVar4);
    ppuVar4 = local_1d0;
    _<>::into_iter(&local_1e8,ppuVar4);
    local_1b8 = local_1e8;
    local_1b0 = local_1e0;
    local_1a8 = local_1d8;
    while (local_1a0 = _<>::next(&local_1b8), local_198 = ppuVar4, ppuVar4 != (undefined **)0x0) {
      local_190 = ppuVar4;
      if (local_1a0 + 1 < local_1a0) {
                    /* WARNING: Subroutine does not return */
        core::panicking::panic_const::panic_const_add_overflow(&PTR_s_main.rs_1400ab460);
      }
      local_158 = local_1a0 + 1;
      core::fmt::rt::Argument::new_display(&local_130,&local_158);
      core::fmt::rt::Argument::new_display(&local_120,&local_190);
      local_150 = local_130;
      local_148 = local_128;
      local_140 = local_120;
      local_138 = local_118;
      ppuVar4 = &PTR_s_Fragment_:_1400ab488;
      core::fmt::rt::_<>::new_v1(local_188,&PTR_s_Fragment_:_1400ab488,&local_150);
      std::io::stdio::_print(local_188);
    }
    core::fmt::rt::_<>::new_const(local_110,&PTR_DAT_1400ab398);
    std::io::stdio::_print(local_110);
    lVar3 = alloc::vec::Vec<T,A>::len(param_1 + 0x18);
    if (lVar3 == 4) {
      ppuVar4 = &PTR_DAT_1400ab3c8;
      core::fmt::rt::_<>::new_const(local_e0,&PTR_DAT_1400ab3c8);
      std::io::stdio::_print(local_e0);
      uVar1 = _<>::deref(param_1 + 0x18);
      alloc::slice::_<impl[T]>::concat(local_b0,uVar1,(longlong)ppuVar4);
      core::fmt::rt::Argument::new_display(&local_50,local_b0);
      local_68 = local_50;
      uStack_60 = uStack_48;
      core::fmt::rt::_<>::new_v1(local_98,&PTR_s_FULL_ARTIFACT:_1400ab3f0,&local_68);
      std::io::stdio::_print(local_98);
      core::ptr::drop_in_place<>((longlong *)local_b0);
    }
    else {
      core::fmt::rt::_<>::new_const(local_40,&PTR_s_[INFO]_collect_all_4_to_reveal_t_1400ab448);
      std::io::stdio::_print(local_40);
    }
  }
  else {
    core::fmt::rt::_<>::new_const(local_2d0,&PTR_DAT_1400ab4d8);
    std::io::stdio::_print(local_2d0);
    core::fmt::rt::_<>::new_const(local_2a0,&PTR_s_[INFO]_clear_trials_to_collect_t_1400ab510);
    std::io::stdio::_print(local_2a0);
  }
  return;
}
```

aaaand that's not the case (`alloc::slice::_<impl[T]>::concat(local_b0,uVar1,(longlong)ppuVar4);`)

Moving onto Trial 1:

```C

/* main::validate_trial_1 */

ulonglong main::validate_trial_1(undefined8 param_1,undefined8 param_2)

{
  undefined8 uVar1;
  longlong lVar2;
  ulonglong uVar3;
  ulonglong uVar4;

  uVar1 = core::str::_<impl_str>::len(param_1,param_2);
  lVar2 = core::hint::black_box(uVar1);
  uVar3 = core::hint::black_box(lVar2 != 8);
  uVar4 = core::hint::black_box(lVar2 == 8);
  return CONCAT71((int7)(uVar4 >> 8),(byte)uVar3 | (byte)uVar4) & 0xffffffffffffff01;
}

```

Section of interest:

```C
    uVar1 = validate_trial_1(uVar3,puVar5);
    if ((uVar1 & 1) == 0) {
      trial_1_victory(param_1);
      core::ptr::drop_in_place<>((longlong *)local_f8);
    }
```

For validate Trial 1:

```C

/* main::validate_trial_1 */

ulonglong main::validate_trial_1(undefined8 param_1,undefined8 param_2)

{
  undefined8 uVar1;
  longlong lVar2;
  ulonglong uVar3;
  ulonglong uVar4;

  uVar1 = core::str::_<impl_str>::len(param_1,param_2);
  lVar2 = core::hint::black_box(uVar1);
  uVar3 = core::hint::black_box(lVar2 != 8);
  uVar4 = core::hint::black_box(lVar2 == 8);
  return CONCAT71((int7)(uVar4 >> 8),(byte)uVar3 | (byte)uVar4) & 0xffffffffffffff01;
}
```

In other words, make sure the input is 8 characters in length? That's what you would do for dynamic analysis I suppose...

I am lazy, so moving onto `validate_trial_1`:

```C

/* main::trial_1_victory */

void main::trial_1_victory(longlong param_1)

{
  uint uVar1;
  ulonglong uVar2;
  undefined8 local_228 [6];
  undefined8 local_1f8 [6];
  undefined8 local_1c8;
  undefined8 uStack_1c0;
  undefined8 local_1b8;
  undefined8 uStack_1b0;
  undefined8 local_1a8 [6];
  undefined8 local_178;
  undefined8 uStack_170;
  undefined8 local_168;
  undefined8 uStack_160;
  ulonglong local_158 [3];
  size_t local_140 [3];
  undefined8 local_128 [6];
  undefined8 local_f8 [6];
  undefined8 local_c8 [6];
  undefined8 local_98 [6];
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40 [8];

  uVar1 = 0x400ab540;
  core::fmt::rt::_<>::new_const(local_228,&PTR_s_[W]_code_accepted_sheesh_1400ab540);
  std::io::stdio::_print(local_228);
  uVar2 = core::time::Duration::from_millis(500);
  std::thread::sleep(uVar2,uVar1);
  core::fmt::rt::Argument::new_display(&local_1b8,&PTR_s_Glitch_Phantom_1400ab588);
  local_1c8 = local_1b8;
  uStack_1c0 = uStack_1b0;
  core::fmt::rt::_<>::new_v1(local_1f8,&PTR_s_[]_nah_u_actually_got_it_1400ab5e8,&local_1c8);
  std::io::stdio::_print(local_1f8);
  core::fmt::rt::Argument::new_display(&local_168,&PTR_s_Glitch_Phantom_1400ab588);
  local_178 = local_168;
  uStack_170 = uStack_160;
  core::fmt::rt::_<>::new_v1(local_1a8,&PTR_s_[]_here_take_this_fragment..._1400ab628,&local_178) ;
  std::io::stdio::_print(local_1a8);
  decrypt_fragment(local_158,&DAT_1400ab648,9);
  _<>::clone(local_140,(longlong)local_158);
  alloc::vec::Vec<T,A>::push((ulonglong *)(param_1 + 0x18),local_140);
  *(undefined1 *)(param_1 + 0x30) = 1;
  uVar1 = *(uint *)(param_1 + 0x34) + 0xfa;
  if (*(uint *)(param_1 + 0x34) <= uVar1) {
    *(uint *)(param_1 + 0x34) = uVar1;
    core::fmt::rt::_<>::new_const(local_128,&PTR_DAT_1400aaff8);
    std::io::stdio::_print(local_128);
    core::fmt::rt::_<>::new_const(local_f8,&PTR_DAT_1400ab6a8);
    std::io::stdio::_print(local_f8);
    core::fmt::rt::_<>::new_const(local_c8,&PTR_DAT_1400ab0e8);
    std::io::stdio::_print(local_c8);
    core::fmt::rt::Argument::new_display(&local_50,local_158);
    local_68 = local_50;
    uStack_60 = uStack_48;
    core::fmt::rt::_<>::new_v1(local_98,&PTR_s_Fragment:_1400ab6c8,&local_68);
    std::io::stdio::_print(local_98);
    core::fmt::rt::_<>::new_const(local_40,&PTR_DAT_1400ab708);
    std::io::stdio::_print(local_40);
    core::ptr::drop_in_place<>((longlong *)local_158);
    return;
  }
                    /* WARNING: Subroutine does not return */
  core::panicking::panic_const::panic_const_add_overflow(&PTR_s_main.rs_1400ab658);
}
```

We then see `decrypt_fragment(local_158,&DAT_1400ab648,9);`

The following data is at `0x1400abc48`:

```
                            DAT_1400ab648                                   XREF[1]:     trial_1_victory:140007d4f (*)
       1400ab648 25              ??         25h    %
       1400ab649 35              ??         35h    5
       1400ab64a 23              ??         23h    #
       1400ab64b 22              ??         22h    "
       1400ab64c 29              ??         29h    )
       1400ab64d 01              ??         01h
       1400ab64e 66              ??         66h    f
       1400ab64f 47              ??         47h    G
       1400ab650 30              ??         30h    0
       1400ab651 00              ??         00h
       1400ab652 00              ??         00h
       1400ab653 00              ??         00h
       1400ab654 00              ??         00h
       1400ab655 00              ??         00h
       1400ab656 00              ??         00h
       1400ab657 00              ??         00h
```

And the following code is at `decrypt_fragment()`:

```C
/* main::decrypt_fragment */

ulonglong * main::decrypt_fragment(ulonglong *param_1,undefined8 param_2,undefined8 param_3)

{
  undefined8 uVar1;
  longlong lVar2;
  undefined8 *puVar3;
  ulonglong local_70 [3];
  undefined8 local_58 [3];
  undefined8 local_40 [3];
  ulonglong local_28 [5];

  uVar1 = core::slice::_<impl[T]>::iter(param_2);
  core::iter::traits::iterator::Iterator::enumerate(local_40,uVar1,param_3);
  puVar3 = local_58;
  core::iter::traits::iterator::Iterator::map(puVar3,local_40);
  core::iter::traits::iterator::Iterator::collect(local_70,puVar3);
  lVar2 = _<>::deref((longlong)local_70);
  alloc::string::String::from_utf8_lossy(local_28,lVar2,(ulonglong)puVar3);
  _<>::to_string(param_1,(longlong *)local_28);
  core::ptr::drop_in_place<>((longlong *)local_70);
  core::ptr::drop_in_place<>((longlong *)local_28);
  return param_1;
}
```

In other words, for each position i: `decrypted[i] = encrypted[i] XOR "CYBERQU3ST"[i % 10]`

And so:
i enc (hex) key[i%10] XOR result char
0 0x25 'C' 0x43 0x66 f
1 0x35 'Y' 0x59 0x6c l
2 0x23 'B' 0x42 0x61 a
3 0x22 'E' 0x45 0x67 g
4 0x29 'R' 0x52 0x7b {
5 0x01 'Q' 0x51 0x50 P
6 0x66 'U' 0x55 0x33 3
7 0x47 '3' 0x33 0x74 t
8 0x30 'S' 0x53 0x63 c

Now for Trial 2!

```C

/* main::trial_2 */

void main::trial_2(longlong param_1)

{
  ulonglong uVar1;
  longlong lVar2;
  void *pvVar3;
  uint uVar4;
  ulonglong *puVar5;
  undefined8 local_390 [6];
  undefined8 local_360 [6];
  undefined8 local_330;
  undefined8 local_328;
  undefined8 local_320;
  undefined8 local_318;
  undefined8 local_310 [6];
  undefined8 local_2e0 [6];
  undefined8 local_2b0 [6];
  undefined8 local_280 [6];
  undefined8 local_250 [6];
  undefined8 local_220 [6];
  undefined8 local_1f0;
  undefined8 local_1e8;
  undefined8 local_1e0;
  undefined8 local_1d8;
  undefined8 local_1d0 [6];
  undefined8 local_1a0;
  undefined8 local_198;
  undefined8 local_190;
  undefined8 local_188;
  undefined8 local_180 [6];
  undefined8 local_150;
  undefined8 local_148;
  undefined8 local_140;
  undefined8 local_138;
  undefined8 local_130 [6];
  undefined8 *local_100;
  ulonglong local_f8 [3];
  undefined *local_e0;
  undefined8 local_d8 [6];
  undefined8 local_a8 [6];
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  longlong local_48;
  longlong local_40 [3];
  ulonglong local_28;
  ulonglong *local_20;
  ulonglong *local_18 [3];

  if ((*(byte *)(param_1 + 0x30) & 1) == 0) {
    core::fmt::rt::_<>::new_const(local_390,&PTR_s_[LOCKED]_u_gotta_clear_Trial_1_f_1400ac150);
    std::io::stdio::_print(local_390);
    core::fmt::rt::Argument::new_display(&local_320,&PTR_s_Glitch_Phantom_1400ab588);
    local_330 = local_320;
    local_328 = local_318;
    core::fmt::rt::_<>::new_v1(local_360,&PTR_s_[INFO]_defeat_to_unlock_this_1400ac180,&local_330 );
    std::io::stdio::_print(local_360);
  }
  else if ((*(byte *)(param_1 + 0x31) & 1) == 0) {
    core::fmt::rt::_<>::new_const(local_2b0,&PTR_DAT_1400aaff8);
    std::io::stdio::_print(local_2b0);
    core::fmt::rt::_<>::new_const(local_280,&PTR_DAT_1400ac1d8);
    std::io::stdio::_print(local_280);
    core::fmt::rt::_<>::new_const(local_250,&PTR_DAT_1400ab0e8);
    std::io::stdio::_print(local_250);
    core::fmt::rt::Argument::new_display(&local_1e0,&PTR_s_Data_Wraith_1400ab598);
    local_1f0 = local_1e0;
    local_1e8 = local_1d8;
    uVar4 = 0x400ac208;
    core::fmt::rt::_<>::new_v1
              (local_220,&PTR_s_[SHEESH]_materialized_from_the_v_1400ac208,&local_1f0);
    std::io::stdio::_print(local_220);
    uVar1 = core::time::Duration::from_millis(800);
    std::thread::sleep(uVar1,uVar4);
    core::fmt::rt::Argument::new_display(&local_190,&PTR_s_Data_Wraith_1400ab598);
    local_1a0 = local_190;
    local_198 = local_188;
    core::fmt::rt::_<>::new_v1(local_1d0,&PTR_s_[]_nah_u_actually_got_it_1400ac248,&local_1a0);
    std::io::stdio::_print(local_1d0);
    core::fmt::rt::Argument::new_display(&local_140,&PTR_s_Data_Wraith_1400ab598);
    local_150 = local_140;
    local_148 = local_138;
    core::fmt::rt::_<>::new_v1(local_180,&PTR_s_[]_here_take_this_fragment..._1400ac290,&local_15 0);
    std::io::stdio::_print(local_180);
    core::fmt::rt::_<>::new_const(local_130,&PTR_DAT_1400abff8);
    std::io::stdio::_print(local_130);
    local_100 = std::io::stdio::stdout();
    local_48 = _<>::flush(&local_100);
    if (local_48 != 0) {
      local_40[0] = local_48;
                    /* WARNING: Subroutine does not return */
      core::result::unwrap_failed
                (&DAT_1400aaf38,0x2b,local_40,&PTR_drop_in_place<std::io::error::Error>_1400aaf18 ,
                 &PTR_s_main.rs_1400ac2b0);
    }
    alloc::string::String::new(local_f8);
    local_e0 = std::io::stdio::stdin();
    puVar5 = local_f8;
    local_28 = std::io::stdio::Stdin::read_line(&local_e0,puVar5);
    local_20 = puVar5;
    if ((local_28 & 1) != 0) {
      local_18[0] = puVar5;
                    /* WARNING: Subroutine does not return */
      core::result::unwrap_failed
                (&DAT_1400aaf38,0x2b,local_18,&PTR_drop_in_place<std::io::error::Error>_1400aaf18 ,
                 &PTR_s_main.rs_1400ac2c8);
    }
    lVar2 = _<>::deref((longlong)local_f8);
    pvVar3 = (void *)core::str::_<impl_str>::trim(lVar2,(ulonglong)puVar5);
    uVar1 = validate_trial_2(pvVar3,(ulonglong)puVar5);
    if ((uVar1 & 1) == 0) {
      trial_2_victory(param_1);
      core::ptr::drop_in_place<>((longlong *)local_f8);
    }
    else {
      core::fmt::rt::_<>::new_const(local_d8,&PTR_s_[L]_code_prefix_is_wrong_ong_1400ac300);
      std::io::stdio::_print(local_d8);
      core::fmt::rt::Argument::new_display(&local_68,&PTR_s_Data_Wraith_1400ab598);
      local_78 = local_68;
      uStack_70 = uStack_60;
      core::fmt::rt::_<>::new_v1(local_a8,&PTR_s_[]_here_take_this_fragment..._1400ac338,&local_7 8);
      std::io::stdio::_print(local_a8);
      core::ptr::drop_in_place<>((longlong *)local_f8);
    }
  }
  else {
    core::fmt::rt::_<>::new_const(local_310,&PTR_s_[INFO]_u_already_cleared_this_tr_1400ac0d8);
    std::io::stdio::_print(local_310);
    core::fmt::rt::_<>::new_const(local_2e0,&PTR_s_[INFO]_fragment_2_is_in_ur_colle_1400ac380);
    std::io::stdio::_print(local_2e0);
  }
  return;
}
```

We observe the same pattern: `validate_trial_2()` followed by `trial_2_victory()`

So `validate_trial_2()` it is:

```C
/* main::validate_trial_2 */

ulonglong main::validate_trial_2(void *param_1,ulonglong param_2)

{
  ulonglong uVar1;
  ulonglong uVar2;

  uVar1 = core::str::_<impl_str>::starts_with(param_1,param_2,&DAT_1400abb30,4);
  uVar1 = core::hint::black_box((byte)uVar1 & 1);
  uVar2 = core::hint::black_box(((byte)uVar1 ^ 0xff) & 1);
  uVar1 = core::hint::black_box((byte)uVar1 & 1);
  return CONCAT71((int7)(uVar1 >> 8),(byte)uVar2 | (byte)uVar1) & 0xffffffffffffff01;
}
```

`core::str::_<impl_str>::starts_with(param_1, param_2, &DAT_1400abb30, 4);` means it checks if the input starts with the data at `0x1400abb30`

At `0x1400abb30`:
DAT_1400abb30 XREF[1]: validate_trial_2:140008984 (*)  
1400abb30 48 ?? 48h H
1400abb31 41 ?? 41h A
1400abb32 43 ?? 43h C
1400abb33 4b ?? 4Bh K

So the input just has to start with `HACK`!

```C
/* main::trial_2_victory */

void main::trial_2_victory(longlong param_1)

{
  uint uVar1;
  ulonglong uVar2;
  undefined8 local_228 [6];
  undefined8 local_1f8 [6];
  undefined8 local_1c8;
  undefined8 uStack_1c0;
  undefined8 local_1b8;
  undefined8 uStack_1b0;
  undefined8 local_1a8 [6];
  undefined8 local_178;
  undefined8 uStack_170;
  undefined8 local_168;
  undefined8 uStack_160;
  ulonglong local_158 [3];
  size_t local_140 [3];
  undefined8 local_128 [6];
  undefined8 local_f8 [6];
  undefined8 local_c8 [6];
  undefined8 local_98 [6];
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40 [8];

  uVar1 = 0x400ab738;
  core::fmt::rt::_<>::new_const(local_228,&PTR_s_[W]_prefix_verified_lets_go_1400ab738);
  std::io::stdio::_print(local_228);
  uVar2 = core::time::Duration::from_millis(500);
  std::thread::sleep(uVar2,uVar1);
  core::fmt::rt::Argument::new_display(&local_1b8,&PTR_s_Data_Wraith_1400ab598);
  local_1c8 = local_1b8;
  uStack_1c0 = uStack_1b0;
  core::fmt::rt::_<>::new_v1(local_1f8,&PTR_s_[]_nah_u_actually_got_it_1400ab760,&local_1c8);
  std::io::stdio::_print(local_1f8);
  core::fmt::rt::Argument::new_display(&local_168,&PTR_s_Data_Wraith_1400ab598);
  local_178 = local_168;
  uStack_170 = uStack_160;
  core::fmt::rt::_<>::new_v1(local_1a8,&PTR_s_[]_here_take_this_fragment..._1400ab7a0,&local_178) ;
  std::io::stdio::_print(local_1a8);
  decrypt_fragment(local_158,&DAT_1400ab7c0,9);
  _<>::clone(local_140,(longlong)local_158);
  alloc::vec::Vec<T,A>::push((ulonglong *)(param_1 + 0x18),local_140);
  *(undefined1 *)(param_1 + 0x31) = 1;
  uVar1 = *(uint *)(param_1 + 0x34) + 0xfa;
  if (*(uint *)(param_1 + 0x34) <= uVar1) {
    *(uint *)(param_1 + 0x34) = uVar1;
    core::fmt::rt::_<>::new_const(local_128,&PTR_DAT_1400aaff8);
    std::io::stdio::_print(local_128);
    core::fmt::rt::_<>::new_const(local_f8,&PTR_DAT_1400ab820);
    std::io::stdio::_print(local_f8);
    core::fmt::rt::_<>::new_const(local_c8,&PTR_DAT_1400ab0e8);
    std::io::stdio::_print(local_c8);
    core::fmt::rt::Argument::new_display(&local_50,local_158);
    local_68 = local_50;
    uStack_60 = uStack_48;
    core::fmt::rt::_<>::new_v1(local_98,&PTR_s_Fragment:_1400ab6c8,&local_68);
    std::io::stdio::_print(local_98);
    core::fmt::rt::_<>::new_const(local_40,&PTR_DAT_1400ab850);
    std::io::stdio::_print(local_40);
    core::ptr::drop_in_place<>((longlong *)local_158);
    return;
  }
                    /* WARNING: Subroutine does not return */
  core::panicking::panic_const::panic_const_add_overflow(&PTR_s_main.rs_1400ab7d0);
}
```

Same, XOR, data at `0x1400ab7d0`:

```
                             DAT_1400ab7c0                                   XREF[1]:     trial_2_victory:140007fff (*)
       1400ab7c0 2b              ??         2Bh    +
       1400ab7c1 78              ??         78h    x
       1400ab7c2 2c              ??         2Ch    ,
       1400ab7c3 02              ??         02h
       1400ab7c4 0d              ??         0Dh
       1400ab7c5 22              ??         22h    "
       1400ab7c6 0a              ??         0Ah
       1400ab7c7 78              ??         78h    x
       1400ab7c8 3a              ??         3Ah    :
       1400ab7c9 00              ??         00h
       1400ab7ca 00              ??         00h
       1400ab7cb 00              ??         00h
       1400ab7cc 00              ??         00h
       1400ab7cd 00              ??         00h
       1400ab7ce 00              ??         00h
       1400ab7cf 00              ??         00h
```

Hence:
i enc (hex) key[i%10] XOR → char
0 0x2b 'C' 0x43 0x68 h
1 0x78 'Y' 0x59 0x21 !
2 0x2c 'B' 0x42 0x6e n
3 0x02 'E' 0x45 0x47 G
4 0x0d 'R' 0x52 0x5f _
5 0x22 'Q' 0x51 0x73 s
6 0x0a 'U' 0x55 0x5f _
7 0x78 '3' 0x33 0x4b K
8 0x3a 'S' 0x53 0x69 i

Key so far: `flag{P3tch!nG_s_Ki`

Next trial!

```C

/* main::trial_3 */

void main::trial_3(longlong param_1)

{
  ulonglong uVar1;
  longlong lVar2;
  void *pvVar3;
  uint uVar4;
  undefined1 **ppuVar5;
  undefined8 local_390 [6];
  undefined8 local_360 [6];
  undefined8 local_330;
  undefined8 local_328;
  undefined8 local_320;
  undefined8 local_318;
  undefined8 local_310 [6];
  undefined8 local_2e0 [6];
  undefined8 local_2b0 [6];
  undefined8 local_280 [6];
  undefined8 local_250 [6];
  undefined8 local_220 [6];
  undefined8 local_1f0;
  undefined8 local_1e8;
  undefined8 local_1e0;
  undefined8 local_1d8;
  undefined8 local_1d0 [6];
  undefined8 local_1a0;
  undefined8 local_198;
  undefined8 local_190;
  undefined8 local_188;
  undefined8 local_180 [6];
  undefined8 local_150;
  undefined8 local_148;
  undefined8 local_140;
  undefined8 local_138;
  undefined8 local_130 [6];
  undefined8 *local_100;
  undefined1 *local_f8 [3];
  undefined *local_e0;
  undefined8 local_d8 [6];
  undefined8 local_a8 [6];
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  longlong local_48;
  longlong local_40 [3];
  ulonglong local_28;
  undefined1 **local_20;
  undefined1 **local_18 [3];

  if ((*(byte *)(param_1 + 0x31) & 1) == 0) {
    core::fmt::rt::_<>::new_const(local_390,&PTR_s_[LOCKED]_u_gotta_clear_Trial_2_f_1400ac3c0);
    std::io::stdio::_print(local_390);
    core::fmt::rt::Argument::new_display(&local_320,&PTR_s_Data_Wraith_1400ab598);
    local_330 = local_320;
    local_328 = local_318;
    core::fmt::rt::_<>::new_v1(local_360,&PTR_s_[INFO]_defeat_to_unlock_this_1400ac180,&local_330 );
    std::io::stdio::_print(local_360);
  }
  else if ((*(byte *)(param_1 + 0x32) & 1) == 0) {
    core::fmt::rt::_<>::new_const(local_2b0,&PTR_DAT_1400aaff8);
    std::io::stdio::_print(local_2b0);
    core::fmt::rt::_<>::new_const(local_280,&PTR_DAT_1400ac408);
    std::io::stdio::_print(local_280);
    core::fmt::rt::_<>::new_const(local_250,&PTR_DAT_1400ab0e8);
    std::io::stdio::_print(local_250);
    core::fmt::rt::Argument::new_display(&local_1e0,&PTR_s_Cipher_Demon_1400ab5a8);
    local_1f0 = local_1e0;
    local_1e8 = local_1d8;
    uVar4 = 0x400ac430;
    core::fmt::rt::_<>::new_v1
              (local_220,&PTR_s_[SHEESH]_materialized_from_the_v_1400ac430,&local_1f0);
    std::io::stdio::_print(local_220);
    uVar1 = core::time::Duration::from_millis(800);
    std::thread::sleep(uVar1,uVar4);
    core::fmt::rt::Argument::new_display(&local_190,&PTR_s_Cipher_Demon_1400ab5a8);
    local_1a0 = local_190;
    local_198 = local_188;
    core::fmt::rt::_<>::new_v1(local_1d0,&PTR_s_[]_nah_u_actually_got_it_1400ac468,&local_1a0);
    std::io::stdio::_print(local_1d0);
    core::fmt::rt::Argument::new_display(&local_140,&PTR_s_Cipher_Demon_1400ab5a8);
    local_150 = local_140;
    local_148 = local_138;
    core::fmt::rt::_<>::new_v1(local_180,&PTR_s_[]_here_take_this_fragment..._1400ac4b0,&local_15 0);
    std::io::stdio::_print(local_180);
    core::fmt::rt::_<>::new_const(local_130,&PTR_DAT_1400abff8);
    std::io::stdio::_print(local_130);
    local_100 = std::io::stdio::stdout();
    local_48 = _<>::flush(&local_100);
    if (local_48 != 0) {
      local_40[0] = local_48;
                    /* WARNING: Subroutine does not return */
      core::result::unwrap_failed
                (&DAT_1400aaf38,0x2b,local_40,&PTR_drop_in_place<std::io::error::Error>_1400aaf18 ,
                 &PTR_s_main.rs_1400ac4d0);
    }
    alloc::string::String::new(local_f8);
    local_e0 = std::io::stdio::stdin();
    ppuVar5 = local_f8;
    local_28 = std::io::stdio::Stdin::read_line(&local_e0,(ulonglong *)ppuVar5);
    local_20 = ppuVar5;
    if ((local_28 & 1) != 0) {
      local_18[0] = ppuVar5;
                    /* WARNING: Subroutine does not return */
      core::result::unwrap_failed
                (&DAT_1400aaf38,0x2b,local_18,&PTR_drop_in_place<std::io::error::Error>_1400aaf18 ,
                 &PTR_s_main.rs_1400ac4e8);
    }
    lVar2 = _<>::deref((longlong)local_f8);
    pvVar3 = (void *)core::str::_<impl_str>::trim(lVar2,(ulonglong)ppuVar5);
    uVar1 = validate_trial_3(pvVar3,ppuVar5);
    if ((uVar1 & 1) == 0) {
      trial_3_victory(param_1);
      core::ptr::drop_in_place<>((longlong *)local_f8);
    }
    else {
      core::fmt::rt::_<>::new_const(local_d8,&PTR_s_[L]_code_pattern_missing_fam_1400ac520);
      std::io::stdio::_print(local_d8);
      core::fmt::rt::Argument::new_display(&local_68,&PTR_s_Cipher_Demon_1400ab5a8);
      local_78 = local_68;
      uStack_70 = uStack_60;
      core::fmt::rt::_<>::new_v1(local_a8,&PTR_s_[]_here_take_this_fragment..._1400ac558,&local_7 8);
      std::io::stdio::_print(local_a8);
      core::ptr::drop_in_place<>((longlong *)local_f8);
    }
  }
  else {
    core::fmt::rt::_<>::new_const(local_310,&PTR_s_[INFO]_u_already_cleared_this_tr_1400ac0d8);
    std::io::stdio::_print(local_310);
    core::fmt::rt::_<>::new_const(local_2e0,&PTR_s_[INFO]_fragment_3_is_in_ur_colle_1400ac5a0);
    std::io::stdio::_print(local_2e0);
  }
  return;
}
```

Validation:

```C

/* main::validate_trial_3 */

ulonglong main::validate_trial_3(void *param_1,undefined1 **param_2)

{
  bool bVar1;
  ulonglong uVar2;
  ulonglong uVar3;

  bVar1 = core::str::_<impl_str>::contains
                    (param_1,param_2,&DAT_1400abb34,(undefined1 **)&DAT_00000005);
  uVar2 = core::hint::black_box(bVar1);
  uVar3 = core::hint::black_box(((byte)uVar2 ^ 0xff) & 1);
  uVar2 = core::hint::black_box((byte)uVar2 & 1);
  return CONCAT71((int7)(uVar2 >> 8),(byte)uVar3 | (byte)uVar2) & 0xffffffffffffff01;
}
```

`core::str::_<impl_str>::contains(param_1,param_2,&DAT_1400abb34,(undefined1 **)&DAT_00000005);` means the string must contain the data at `0x1400abb34`

Data:

```
                             DAT_1400abb34                                   XREF[1]:     validate_trial_3:1400089d4 (*)
       1400abb34 5f              ??         5Fh    _
       1400abb35 58              ??         58h    X
       1400abb36 30              ??         30h    0
       1400abb37 58              ??         58h    X
       1400abb38 5f              ??         5Fh    _
```

So the string must contain the substring `_XOX_` anywhere!

Victory:

```C

/* main::trial_3_victory */

void main::trial_3_victory(longlong param_1)

{
  uint uVar1;
  ulonglong uVar2;
  undefined8 local_228 [6];
  undefined8 local_1f8 [6];
  undefined8 local_1c8;
  undefined8 uStack_1c0;
  undefined8 local_1b8;
  undefined8 uStack_1b0;
  undefined8 local_1a8 [6];
  undefined8 local_178;
  undefined8 uStack_170;
  undefined8 local_168;
  undefined8 uStack_160;
  ulonglong local_158 [3];
  size_t local_140 [3];
  undefined8 local_128 [6];
  undefined8 local_f8 [6];
  undefined8 local_c8 [6];
  undefined8 local_98 [6];
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40 [8];

  uVar1 = 0x400ab880;
  core::fmt::rt::_<>::new_const(local_228,&PTR_s_[W]_pattern_detected_valid_1400ab880);
  std::io::stdio::_print(local_228);
  uVar2 = core::time::Duration::from_millis(500);
  std::thread::sleep(uVar2,uVar1);
  core::fmt::rt::Argument::new_display(&local_1b8,&PTR_s_Cipher_Demon_1400ab5a8);
  local_1c8 = local_1b8;
  uStack_1c0 = uStack_1b0;
  core::fmt::rt::_<>::new_v1(local_1f8,&PTR_s_[]_nah_u_actually_got_it_1400ab8b8,&local_1c8);
  std::io::stdio::_print(local_1f8);
  core::fmt::rt::Argument::new_display(&local_168,&PTR_s_Cipher_Demon_1400ab5a8);
  local_178 = local_168;
  uStack_170 = uStack_160;
  core::fmt::rt::_<>::new_v1(local_1a8,&PTR_s_[]_here_take_this_fragment..._1400ab8f8,&local_178) ;
  std::io::stdio::_print(local_1a8);
  decrypt_fragment(local_158,&DAT_1400ab918,9);
  _<>::clone(local_140,(longlong)local_158);
  alloc::vec::Vec<T,A>::push((ulonglong *)(param_1 + 0x18),local_140);
  *(undefined1 *)(param_1 + 0x32) = 1;
  uVar1 = *(uint *)(param_1 + 0x34) + 0xfa;
  if (*(uint *)(param_1 + 0x34) <= uVar1) {
    *(uint *)(param_1 + 0x34) = uVar1;
    core::fmt::rt::_<>::new_const(local_128,&PTR_DAT_1400aaff8);
    std::io::stdio::_print(local_128);
    core::fmt::rt::_<>::new_const(local_f8,&PTR_DAT_1400ab978);
    std::io::stdio::_print(local_f8);
    core::fmt::rt::_<>::new_const(local_c8,&PTR_DAT_1400ab0e8);
    std::io::stdio::_print(local_c8);
    core::fmt::rt::Argument::new_display(&local_50,local_158);
    local_68 = local_50;
    uStack_60 = uStack_48;
    core::fmt::rt::_<>::new_v1(local_98,&PTR_s_Fragment:_1400ab6c8,&local_68);
    std::io::stdio::_print(local_98);
    core::fmt::rt::_<>::new_const(local_40,&PTR_DAT_1400ab9a8);
    std::io::stdio::_print(local_40);
    core::ptr::drop_in_place<>((longlong *)local_158);
    return;
  }
                    /* WARNING: Subroutine does not return */
  core::panicking::panic_const::panic_const_add_overflow(&PTR_s_main.rs_1400ab928);
}
```

Data:

```
                             DAT_1400ab918                                   XREF[1]:     trial_3_victory:1400082af (*)
       1400ab918 2d              ??         2Dh    -
       1400ab919 3d              ??         3Dh    =
       1400ab91a 31              ??         31h    1
       1400ab91b 1a              ??         1Ah
       1400ab91c 11              ??         11h
       1400ab91d 61              ??         61h    a
       1400ab91e 65              ??         65h    e
       1400ab91f 5c              ??         5Ch    \
       1400ab920 1c              ??         1Ch
       1400ab921 00              ??         00h
       1400ab922 00              ??         00h
       1400ab923 00              ??         00h
       1400ab924 00              ??         00h
       1400ab925 00              ??         00h
       1400ab926 00              ??         00h
       1400ab927 00              ??         00h
```

Fragment:
i enc (hex) key[i%10] XOR → char
0 0x2d 'C' 0x43 0x6e n
1 0x3d 'Y' 0x59 0x64 d
2 0x31 'B' 0x42 0x73 s
3 0x1a 'E' 0x45 0x50 P
4 0x11 'R' 0x52 0x43 C
5 0x61 'Q' 0x51 0x30 0
6 0x65 'U' 0x55 0x30 0
7 0x5c '3' 0x33 0x6f o
8 0x1c 'S' 0x53 0x70 p

Flag so far: flag{P3tch!nG_s_KindsPC00op

Last trial:

```C
/* main::trial_4 */

void main::trial_4(longlong param_1)

{
  ulonglong uVar1;
  longlong lVar2;
  undefined8 uVar3;
  uint uVar4;
  ulonglong *puVar5;
  undefined8 local_390 [6];
  undefined8 local_360 [6];
  undefined8 local_330;
  undefined8 local_328;
  undefined8 local_320;
  undefined8 local_318;
  undefined8 local_310 [6];
  undefined8 local_2e0 [6];
  undefined8 local_2b0 [6];
  undefined8 local_280 [6];
  undefined8 local_250 [6];
  undefined8 local_220 [6];
  undefined8 local_1f0;
  undefined8 local_1e8;
  undefined8 local_1e0;
  undefined8 local_1d8;
  undefined8 local_1d0 [6];
  undefined8 local_1a0;
  undefined8 local_198;
  undefined8 local_190;
  undefined8 local_188;
  undefined8 local_180 [6];
  undefined8 local_150;
  undefined8 local_148;
  undefined8 local_140;
  undefined8 local_138;
  undefined8 local_130 [6];
  undefined8 *local_100;
  ulonglong local_f8 [3];
  undefined *local_e0;
  undefined8 local_d8 [6];
  undefined8 local_a8 [6];
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  longlong local_48;
  longlong local_40 [3];
  ulonglong local_28;
  ulonglong *local_20;
  ulonglong *local_18 [3];

  if ((*(byte *)(param_1 + 0x32) & 1) == 0) {
    core::fmt::rt::_<>::new_const(local_390,&PTR_s_[LOCKED]_u_gotta_clear_Trial_3_f_1400ac5e0);
    std::io::stdio::_print(local_390);
    core::fmt::rt::Argument::new_display(&local_320,&PTR_s_Cipher_Demon_1400ab5a8);
    local_330 = local_320;
    local_328 = local_318;
    core::fmt::rt::_<>::new_v1(local_360,&PTR_s_[INFO]_defeat_to_unlock_this_1400ac180,&local_330 );
    std::io::stdio::_print(local_360);
  }
  else if ((*(byte *)(param_1 + 0x33) & 1) == 0) {
    core::fmt::rt::_<>::new_const(local_2b0,&PTR_DAT_1400aaff8);
    std::io::stdio::_print(local_2b0);
    core::fmt::rt::_<>::new_const(local_280,&PTR_DAT_1400ac628);
    std::io::stdio::_print(local_280);
    core::fmt::rt::_<>::new_const(local_250,&PTR_DAT_1400ab0e8);
    std::io::stdio::_print(local_250);
    core::fmt::rt::Argument::new_display(&local_1e0,&PTR_s_Sigma_Guardian_1400ab5b8);
    local_1f0 = local_1e0;
    local_1e8 = local_1d8;
    uVar4 = 0x400ac658;
    core::fmt::rt::_<>::new_v1
              (local_220,&PTR_s_[SHEESH]_materialized_from_the_v_1400ac658,&local_1f0);
    std::io::stdio::_print(local_220);
    uVar1 = core::time::Duration::from_millis(800);
    std::thread::sleep(uVar1,uVar4);
    core::fmt::rt::Argument::new_display(&local_190,&PTR_s_Sigma_Guardian_1400ab5b8);
    local_1a0 = local_190;
    local_198 = local_188;
    core::fmt::rt::_<>::new_v1(local_1d0,&PTR_s_[]_nah_u_actually_got_it_1400ac698,&local_1a0);
    std::io::stdio::_print(local_1d0);
    core::fmt::rt::Argument::new_display(&local_140,&PTR_s_Sigma_Guardian_1400ab5b8);
    local_150 = local_140;
    local_148 = local_138;
    core::fmt::rt::_<>::new_v1(local_180,&PTR_s_[]_here_take_this_fragment..._1400ac6f0,&local_15 0);
    std::io::stdio::_print(local_180);
    core::fmt::rt::_<>::new_const(local_130,&PTR_DAT_1400abff8);
    std::io::stdio::_print(local_130);
    local_100 = std::io::stdio::stdout();
    local_48 = _<>::flush(&local_100);
    if (local_48 != 0) {
      local_40[0] = local_48;
                    /* WARNING: Subroutine does not return */
      core::result::unwrap_failed
                (&DAT_1400aaf38,0x2b,local_40,&PTR_drop_in_place<std::io::error::Error>_1400aaf18 ,
                 &PTR_s_main.rs_1400ac710);
    }
    alloc::string::String::new(local_f8);
    local_e0 = std::io::stdio::stdin();
    puVar5 = local_f8;
    local_28 = std::io::stdio::Stdin::read_line(&local_e0,puVar5);
    local_20 = puVar5;
    if ((local_28 & 1) != 0) {
      local_18[0] = puVar5;
                    /* WARNING: Subroutine does not return */
      core::result::unwrap_failed
                (&DAT_1400aaf38,0x2b,local_18,&PTR_drop_in_place<std::io::error::Error>_1400aaf18 ,
                 &PTR_s_main.rs_1400ac728);
    }
    lVar2 = _<>::deref((longlong)local_f8);
    uVar3 = core::str::_<impl_str>::trim(lVar2,(ulonglong)puVar5);
    uVar1 = validate_trial_4(uVar3,(ulonglong)puVar5);
    if ((uVar1 & 1) == 0) {
      trial_4_victory(param_1);
      core::ptr::drop_in_place<>((longlong *)local_f8);
    }
    else {
      core::fmt::rt::_<>::new_const(local_d8,&PTR_s_[L]_code_power_level_aint_500_fa_1400ac768);
      std::io::stdio::_print(local_d8);
      core::fmt::rt::Argument::new_display(&local_68,&PTR_s_Sigma_Guardian_1400ab5b8);
      local_78 = local_68;
      uStack_70 = uStack_60;
      core::fmt::rt::_<>::new_v1(local_a8,&PTR_s_[]_here_take_this_fragment..._1400ac790,&local_7 8);
      std::io::stdio::_print(local_a8);
      core::ptr::drop_in_place<>((longlong *)local_f8);
    }
  }
  else {
    core::fmt::rt::_<>::new_const(local_310,&PTR_s_[INFO]_u_already_cleared_this_tr_1400ac0d8);
    std::io::stdio::_print(local_310);
    core::fmt::rt::_<>::new_const(local_2e0,&PTR_s_[INFO]_fragment_4_is_in_ur_colle_1400ac7d8);
    std::io::stdio::_print(local_2e0);
  }
  return;
}
```

Validate:

```C
/* main::validate_trial_4 */

ulonglong main::validate_trial_4(undefined8 param_1,ulonglong param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined8 uVar3;
  longlong lVar4;
  ulonglong uVar5;
  ulonglong uVar6;

  uVar3 = core::str::_<impl_str>::chars(param_1);
  lVar4 = core::iter::traits::iterator::Iterator::map(uVar3);
  uVar1 = core::iter::traits::iterator::Iterator::sum(lVar4,param_2);
  iVar2 = core::hint::black_box(uVar1);
  uVar5 = core::hint::black_box(iVar2 != 500);
  uVar6 = core::hint::black_box(iVar2 == 500);
  return CONCAT71((int7)(uVar6 >> 8),(byte)uVar5 | (byte)uVar6) & 0xffffffffffffff01;
}
```

There is no data section to reference here, map() just gives the character value of the input, while the `!=` and `==` operators signify that the sum of the input should be equal to 500

If you an exact breakdown of how it works from the AI:

- The closure at 140008a80 does MOV EAX, param_2; RET, so it just returns the character value (each char as a u32)
- CMP EAX, 0x1f4 → compare the sum to 500 (0x1f4)

Victory:

```C

/* main::trial_4_victory */

void main::trial_4_victory(longlong param_1)

{
  uint uVar1;
  ulonglong uVar2;
  undefined8 local_228 [6];
  undefined8 local_1f8 [6];
  undefined8 local_1c8;
  undefined8 uStack_1c0;
  undefined8 local_1b8;
  undefined8 uStack_1b0;
  undefined8 local_1a8 [6];
  undefined8 local_178;
  undefined8 uStack_170;
  undefined8 local_168;
  undefined8 uStack_160;
  ulonglong local_158 [3];
  size_t local_140 [3];
  undefined8 local_128 [6];
  undefined8 local_f8 [6];
  undefined8 local_c8 [6];
  undefined8 local_98 [6];
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40 [8];

  uVar1 = 0x400ab9e0;
  core::fmt::rt::_<>::new_const(local_228,&PTR_s_[W]_power_level_verified_sigma_e_1400ab9e0);
  std::io::stdio::_print(local_228);
  uVar2 = core::time::Duration::from_millis(500);
  std::thread::sleep(uVar2,uVar1);
  core::fmt::rt::Argument::new_display(&local_1b8,&PTR_s_Sigma_Guardian_1400ab5b8);
  local_1c8 = local_1b8;
  uStack_1c0 = uStack_1b0;
  core::fmt::rt::_<>::new_v1(local_1f8,&PTR_s_[]_nah_u_actually_got_it_1400aba10,&local_1c8);
  std::io::stdio::_print(local_1f8);
  core::fmt::rt::Argument::new_display(&local_168,&PTR_s_Sigma_Guardian_1400ab5b8);
  local_178 = local_168;
  uStack_170 = uStack_160;
  core::fmt::rt::_<>::new_v1(local_1a8,&PTR_s_[]_here_take_this_fragment..._1400aba50,&local_178) ;
  std::io::stdio::_print(local_1a8);
  decrypt_fragment(local_158,&DAT_1400aba70,8);
  _<>::clone(local_140,(longlong)local_158);
  alloc::vec::Vec<T,A>::push((ulonglong *)(param_1 + 0x18),local_140);
  *(undefined1 *)(param_1 + 0x33) = 1;
  uVar1 = *(uint *)(param_1 + 0x34) + 0xfa;
  if (*(uint *)(param_1 + 0x34) <= uVar1) {
    *(uint *)(param_1 + 0x34) = uVar1;
    core::fmt::rt::_<>::new_const(local_128,&PTR_DAT_1400aaff8);
    std::io::stdio::_print(local_128);
    core::fmt::rt::_<>::new_const(local_f8,&PTR_DAT_1400abac8);
    std::io::stdio::_print(local_f8);
    core::fmt::rt::_<>::new_const(local_c8,&PTR_DAT_1400ab0e8);
    std::io::stdio::_print(local_c8);
    core::fmt::rt::Argument::new_display(&local_50,local_158);
    local_68 = local_50;
    uStack_60 = uStack_48;
    core::fmt::rt::_<>::new_v1(local_98,&PTR_s_Fragment:_1400ab6c8,&local_68);
    std::io::stdio::_print(local_98);
    uVar1 = 0x400abaf8;
    core::fmt::rt::_<>::new_const(local_40,&PTR_DAT_1400abaf8);
    std::io::stdio::_print(local_40);
    uVar2 = core::time::Duration::from_millis(1000);
    std::thread::sleep(uVar2,uVar1);
    reveal_full_artifact(param_1);
    core::ptr::drop_in_place<>((longlong *)local_158);
    return;
  }
                    /* WARNING: Subroutine does not return */
  core::panicking::panic_const::panic_const_add_overflow(&PTR_s_main.rs_1400aba78);
}
```

Data:

```
                             DAT_1400aba70                                   XREF[1]:     trial_4_victory:14000855f (*)
       1400aba70 73              ??         73h    s
       1400aba71 16              ??         16h
       1400aba72 0d              ??         0Dh
       1400aba73 09              ??         09h
       1400aba74 0d              ??         0Dh
       1400aba75 18              ??         18h
       1400aba76 12              ??         12h
       1400aba77 4e              ??         4Eh    N
```

Which gives us:
`i enc (hex) key[i%10] XOR → char
0 0x73 'C' 0x43 0x30 0
1 0x16 'Y' 0x59 0x4e n
2 0x0d 'B' 0x42 0x4f o
3 0x09 'E' 0x45 0x4c L
4 0x0d 'R' 0x52 0x5f _
5 0x18 'Q' 0x51 0x49 I
6 0x12 'U' 0x55 0x47 G
7 0x4e '3' 0x33 0x7d }

Last fragment: `0noL_IG}`
Eventual Flag: `flag{P3tch!nG_s_KindsPC00op0noL_IG}`

- I am too lazy to verify the actual XOR'ed flag, GPT says it's `flag{P3tch!nG_s_Kinds_C00oO0OOL_IG}` which looks way more correct
