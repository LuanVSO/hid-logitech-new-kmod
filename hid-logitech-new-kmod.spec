# (un)define the next line to either build for the newest or all current kernels
#global buildforkernels newest
#global buildforkernels current
%global buildforkernels akmod
%global module hid-logitech-new
%global projname new-lg4ff
%global debug_package %{nil}

# name should have a -kmod suffix
Name:          %{module}-kmod

Version:        0.5.0
Release:        9%{?dist}
Summary:        Improved module driver for Logitech driving wheels
Epoch:          0
Group:          System Environment/Kernel

License:        GPL-2.0-only
URL:            https://github.com/berarma/new-lg4ff
Source0:        %{url}/archive/v%{version}/%{projname}-%{version}.tar.gz

BuildRequires: kmodtool, gcc
Requires: akmods
Provides: %{projname} = %{version}-%{release}
Obsoletes: %{projname} < 0.5.0
# Verify that the package build for all architectures.
# In most time you should remove the Exclusive/ExcludeArch directives
# and fix the code (if needed).
# ExclusiveArch:  i686 x86_64 ppc64 ppc64le armv7hl aarch64
# ExcludeArch: i686 x86_64 ppc64 ppc64le armv7hl aarch64

BuildRequires: kernel-devel, gcc, make
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{module} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%package common
Summary: License and documentation for %{module}-kmod
source1: modprobe-d-99-hid-logitech-blacklist.conf
source2: modules-load-d-hid-logitech-new.conf
BuildRequires: systemd-rpm-macros
%files common
%doc %{projname}-%{version}/README.md
%license %{projname}-%{version}/LICENSE
%{_modprobedir}/98-hid-logitech-blacklist.conf
%{_modulesloaddir}/hid-logitech-new.conf
%description common
Configuration, license and documentation for %{module}-kmod

%description
Improved Linux module driver for Logitech driving wheels.

Thanks to Oleg Makarenko for adding support for the Logitech G923 Racing Wheel.

Supported devices:

Logitech WingMan Formula GP (without force feedback)
Logitech WingMan Formula Force GP
Logitech Driving Force
Logitech MOMO Force Feedback Racing Wheel
Logitech Driving Force Pro
Logitech G25 Racing Wheel
Logitech Driving Force GT
Logitech G27 Racing Wheel
Logitech G29 Driving Force (switch in PS3 mode)
Logitech G923 Racing Wheel for PlayStation 4 and PC (046d:c267, 046d:c266)
Logitech MOMO Racing
Logitech Speed Force Wireless Wheel for Wii

Differences with the in-tree module
It has all the features in the in-kernel hid-logitech module and adds the
following ones:

Support for most effects defined in the Linux FF API (except inertia) rather
than just constant the force effect.
Asynchronous operations with realtime handling of effects.
Rate limited FF updates with best possible latency.
configurable sprint, damper and friction effects gain.
It can combine accelerator and clutch.
Use the wheel led's as a FFBmeter to monitor clipping.
Added a system gain setting that modulates the gain setting used by applications
SYSFS entries for gain, auto center, spring/damper/friction effect
gain and FFBmeter

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{module} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

for kernel_version in %{?kernel_versions} ; do
    cp -a %{projname}-%{version} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
    %make_build V=1 -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done

%install
install -D -m 0644 %{SOURCE1} %{buildroot}%{_modprobedir}/98-hid-logitech-blacklist.conf
install -D -m 0644 %{SOURCE2} %{buildroot}%{_modulesloaddir}/hid-logitech-new.conf

for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -D -m 755 _kmod_build_${kernel_version%%___*}/%{module}.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
done
%{?akmod_install}

%changelog
* Fri Jul 18 2025 Luan Vitor Simião oliveira <luanv.oliveira@outlook.com> 0.5.0-9
- fix build (luanv.oliveira@outlook.com)

* Fri Jul 18 2025 Luan Vitor Simião oliveira <luanv.oliveira@outlook.com> 0.5.0-8
- use buildroot instead of / (luanv.oliveira@outlook.com)

* Fri Jul 18 2025 Luan Vitor Simião oliveira <luanv.oliveira@outlook.com> 0.5.0-7
- fix build by adding leading / (luanv.oliveira@outlook.com)

* Fri Jul 18 2025 Luan Vitor Simião oliveira <luanv.oliveira@outlook.com> 0.5.0-6
- add modprobe config files to prevent upstream driver being used (luanv.oliveira@outlook.com)

* Thu Jul 17 2025 Luan Vitor Simião oliveira <luanv.oliveira@outlook.com> 0.5.0-5
- rpmlint fixes (luanv.oliveira@outlook.com)

* Wed Jul 16 2025 Luan Vitor Simião oliveira <luanv.oliveira@outlook.com> 0.5.0-4
- general improvments to spec file (luanv.oliveira@outlook.com)
- include license and readme on package (luanv.oliveira@outlook.com)
- fix punctuation and white space fixes (luanv.oliveira@outlook.com)
- remove clean section (luanv.oliveira@outlook.com)
- fix: license information (luanv.oliveira@outlook.com)

* Wed Jul 16 2025 Luan Oliveira <luanv.oliveira@outlook.com> - 0.5.0-2
- merge hid-logitech-new-common into main spec file

* Wed Jul 16 2025 Luan Oliveira <luanv.oliveira@outlook.com> - 0.5.0
- Initial spec with akmod for 0.5.0
