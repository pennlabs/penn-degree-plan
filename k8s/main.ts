import { Construct } from 'constructs';
import { App } from 'cdk8s';
import { DjangoApplication, PennLabsChart, ReactApplication, RedisApplication } from '@pennlabs/kittyhawk';


export class MyChart extends PennLabsChart {
  constructor(scope: Construct) {
    super(scope);

    const backendImage = 'pennlabs/penn-degree-plan-backend';
    const secret = 'penn-courses';
    const ingressProps = {
      annotations: {
        ['ingress.kubernetes.io/content-security-policy']: "frame-ancestors 'none';",
        ["ingress.kubernetes.io/protocol"]: "https",
        ["traefik.ingress.kubernetes.io/router.middlewares"]: "default-redirect-http@kubernetescrd"
      }
    }

    new RedisApplication(this, 'redis', {
      persistData: true,
    });

    new DjangoApplication(this, 'celery', {
      deployment: {
        image: backendImage,
        secret,
        cmd: ['celery', 'worker', '-A', 'PennCourses', '-Q', 'alerts,celery', '-linfo'],
      },
      djangoSettingsModule: 'PennCourses.settings.production',
    });

    new DjangoApplication(this, 'backend', {
      deployment: {
        image: backendImage,
        secret,
        replicas: 5,
      },
      djangoSettingsModule: 'PennCourses.settings.production',
      ingressProps,
      domains: [{ host: 'penncourseplan.com', paths: ["/api", "/admin", "/accounts", "/assets"] },
      { host: 'penncoursealert.com', paths: ["/api", "/admin", "/accounts", "/assets", "/webhook"] },
      { host: 'penncoursereview.com', paths: ["/api", "/admin", "/accounts", "/assets"] }],
    });

    new DjangoApplication(this, 'backend-asgi', {
      deployment: {
        image: backendImage,
        cmd: ['/usr/local/bin/asgi-run'],
        secret,
        replicas: 1,
      },
      djangoSettingsModule: 'PennCourses.settings.production',
      ingressProps,
      domains: [{ host: 'penncoursereview.com', paths: ["/api/ws"] }],
    });

    new ReactApplication(this, 'degree-plan', {
      deployment: {
        image: 'pennlabs/pdp-frontend',
      },
      domain: { host: 'penndegreeplan.com', paths: ['/'] },
    });
  }
}

const app = new App();
new MyChart(app);
app.synth();
