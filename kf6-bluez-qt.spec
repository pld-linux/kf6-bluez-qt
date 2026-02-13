#
# Conditional build:
%bcond_with	tests		# build without tests
#
%define		kdeframever	6.23
%define		qtver		5.15.2
%define		kfname		bluez-qt
Summary:	Qt wrapper for Bluez 5 DBus API
Name:		kf6-%{kfname}
Version:	6.23.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	2b90def0079acc96566631caf35ddcbd
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt wrapper for Bluez 5 DBus API.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%{?with_tests:%ninja_build -C build test}


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/libKF6BluezQt.so.*.*.*
%ghost %{_libdir}/libKF6BluezQt.so.6
%dir %{_libdir}/qt6/qml/org/kde/bluezqt
%{_libdir}/qt6/qml/org/kde/bluezqt/qmldir
%{_libdir}/qt6/qml/org/kde/bluezqt/DevicesModel.qml
%{_libdir}/qt6/qml/org/kde/bluezqt/libbluezqtextensionplugin.so
%{_datadir}/qlogging-categories6/bluezqt.categories
%{_datadir}/qlogging-categories6/bluezqt.renamecategories
%{_libdir}/qt6/qml/org/kde/bluezqt/bluezqtextensionplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/bluezqt/kde-qmlmodule.version

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF6BluezQt.so
%{_includedir}/KF6/BluezQt
%{_libdir}/cmake/KF6BluezQt
%{_pkgconfigdir}/KF6BluezQt.pc
