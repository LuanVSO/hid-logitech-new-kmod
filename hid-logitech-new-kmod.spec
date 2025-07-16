# (un)define the next line to either build for the newest or all current kernels
#define buildforkernels newest
#define buildforkernels current
%global buildforkernels akmod
%define module hid-logitech-new
%global projname new-lg4ff
%global debug_package %{nil}

# name should have a -kmod suffix
Name:          %{module}-kmod

Version:        0.5.0
Release:        1%{?dist}
Summary:        Improved module driver for Logitech driving wheels.
Epoch:          0
Group:          System Environment/Kernel

License:        GPLv3
URL:            https://github.com/berarma/new-lg4ff
Source0:        %{url}/archive/v%{version}/%{projname}-%{version}.tar.gz

BuildRequires: kmodtool, gcc


# Verify that the package build for all architectures.
# In most time you should remove the Exclusive/ExcludeArch directives
# and fix the code (if needed).
# ExclusiveArch:  i686 x86_64 ppc64 ppc64le armv7hl aarch64
# ExcludeArch: i686 x86_64 ppc64 ppc64le armv7hl aarch64

# get the proper build-sysbuild package from the repo, which
# tracks in all the kernel-devel packages
BuildRequires: kernel-devel, gcc, make
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{module} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
Improved module driver for Logitech driving wheels.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{module} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

# apply patches and do other stuff here
# pushd foo-%{version}
# #patch0 -p1 -b .suffix
# popd

for kernel_version in %{?kernel_versions} ; do
    cp -a %{projname}-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
    make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done


%install
#rm -rf ${RPM_BUILD_ROOT}

for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -D -m 755 _kmod_build_${kernel_version%%___*}/%{module}.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
    #make install DESTDIR=${RPM_BUILD_ROOT} KMODPATH=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
    # install -D -m 755 _kmod_build_${kernel_version%%___*}/foo/foo.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/foo.ko
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Jul 16 2025 Luan Oliveira <luanv.oliveira@outlook.com> - 0.5.0
- Initial spec with akmod for 0.5.0
